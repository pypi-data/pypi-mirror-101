/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import withStyles, { CSSProperties } from '@material-ui/core/styles/withStyles';
import { TextBox, SubHeader } from '../../core';
import { OutlinedInput, IconButton, Accordion, AccordionSummary, AccordionDetails, withTheme, Theme } from '@material-ui/core';
import { Global } from '../../Global';
import { FileUploadConfig } from '../../models/FileUploadConfig';
import CloseIcon from '@material-ui/icons/Close'
import { UploadConfig } from '../../models/UploadConfig';
import FileServerUtils from '../../utils/FileServerUtils';
import { OptumiMetadataTracker } from '../../models/OptumiMetadataTracker';
import { AddFilesPopup } from './AddFilesPopup';
import DirListingItemIcon from './fileBrowser/DirListingItemIcon';
import { FileMetadata } from './fileBrowser/FileBrowser';
import { DataConnectorMetadata } from './dataConnectorBrowser/DataConnectorBrowser';
import { AddDataConnectorsPopup } from './AddDataConnectorsPopup';
import { DataConnectorUploadConfig } from '../../models/DataConnectorUploadConfig';

import { ServerConnection } from '@jupyterlab/services';
import DataConnectorDirListingItemIcon from './dataConnectorBrowser/DataConnectorDirListingItemIcon';
import { ExpandMore, WarningRounded } from '@material-ui/icons';
import { NotificationsPopup } from './NotificationsPopup';

// const emDirNotFile = 'Path is a directory, not a file'
// const emDupPath = 'Duplicate file or directory'
// const emNoPath = 'Unable to find file or directory'

// const bounceAnimation = 'all 333ms cubic-bezier(0.33, 1.33, 0.66, 1) 0s'
const easeAnimation = 'all 150ms ease 0s'

const StyledAccordion = withStyles({
    root: {
        borderWidth: '0px',
        '&.Mui-expanded': {
            margin: '0px',
        },
        '&:before': {
            backgroundColor: 'unset',
        },
    },
})(Accordion)

const StyledAccordionSummary = withStyles({
    root: {
        padding: '0px',
        minHeight: '0px',
        '&.Mui-expanded': {
            minHeight: '0px',
        },
    },
    content: {
        margin: '0px',
        '&.Mui-expanded': {
            margin: '0px',
        },
    },
    expandIcon: {
        padding: '0px',
        marginRight: '0px',
    },
})(AccordionSummary)

const StyledAccordionDetails = withStyles({
    root: {
        display: 'flex',
        flexDirection: 'column',
        padding: '0px',
    },
})(AccordionDetails)

interface IProps {
    style?: CSSProperties
    openUserDialogTo?: (page: number) => Promise<void> // This is somewhat spaghetti code-y, maybe think about revising
    theme: Theme
}

interface IState {
    filePath: string
    // Here is where we will keep a list of the file paths that were entered successfully but no longer exist on the disk
    problemFiles: string[]
    problemDataConnectors: string[]
    packagesExpanded: boolean
    filesExpanded: boolean
}

class FilesPanel extends React.Component<IProps, IState> {
    private _isMounted = false

    StyledOutlinedInput: any
    textField: React.RefObject<HTMLInputElement>
    timeout: NodeJS.Timeout
    refreshingFiles: boolean
    refreshingDataConnectors: boolean

    constructor(props: IProps) {
        super(props)
        this.StyledOutlinedInput = this.getStyledOutlinedInput()
        this.textField = React.createRef()
        this.state = {
            filePath: '',
            problemFiles: [],
            problemDataConnectors: [],
            packagesExpanded: false,
            filesExpanded: false,
        }
    }

    private getStyledOutlinedInput = () => {
        return withStyles({
            root: {
                backgroundColor: 'var(--jp-layout-color1)'
            },
            input: {
                fontSize: '12px',
                padding: '3px 6px 3px 6px',
            },
        }) (OutlinedInput);
    }

    private getRequirementsValue = () => {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const uploads: UploadConfig = optumi.config.upload;
        return uploads.requirements;
    }

    private saveRequirements = (value: string): string => {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const uploads: UploadConfig = optumi.config.upload;
        uploads.requirements = value;
        tracker.setMetadata(optumi);
        return '';
    }

    private pathHasError = (path: string): boolean => {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const upload: UploadConfig = optumi.config.upload;
        const files = upload.files;
        for (var i = 0; i < files.length; i++) {
            if (files[i].path === path) return true;
        }
        return false;
    }

    private nameHasError = (name: string): boolean => {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const upload: UploadConfig = optumi.config.upload;
        const dataConnectors = upload.dataConnectors;
        for (var i = 0; i < dataConnectors.length; i++) {
            if (dataConnectors[i].name === name) return true;
        }
        return false;
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const optumi = Global.metadata.getMetadata().config;
        const files = optumi.upload.files;
        const dataConnectors = optumi.upload.dataConnectors;
        return (
            <div style={this.props.style}>
                <StyledAccordion
                    variant={'outlined'}
                    expanded={this.state.packagesExpanded}
                    style={{background: 'var(--jp-layout-color1)'}}
                >
                    <StyledAccordionSummary style={{cursor: 'default'}}>
                        <SubHeader title='Packages' />
                        <span style={{
                            margin: 'auto 15px',
                            flexGrow: 1,
                            textAlign: 'end',
                            opacity: this.state.packagesExpanded ? 0 : 0.5,
                            transitionDuration: '217ms',
                            whiteSpace: 'nowrap',
                            fontSize: '12px',
                            fontStyle: 'italic',
                        }}>
                            {(() => {
                                const requirements = optumi.upload.requirements
                                const numRequirements = requirements === '' ? 0 : requirements.split('\n').filter(line => line !== '').length
                                if (numRequirements > 0) {
                                    return numRequirements + ' requirement' + (numRequirements > 1 ? 's' : '')
                                }
                            })()}
                        </span>
                        <IconButton
                            onClick={() => this.safeSetState({packagesExpanded: !this.state.packagesExpanded})}
                            style={{padding: '0px', marginRight: '-3px', width: '30px'}}
                        >
                            <ExpandMore />
                        </IconButton>
                    </StyledAccordionSummary>
                    <StyledAccordionDetails>
                        <div style={{display: 'flex', width: '100%'}}>
                            <TextBox<string>
                                key={optumi.upload.requirements}
                                multiline
                                getValue={this.getRequirementsValue}
                                saveValue={this.saveRequirements}
                                placeholder={'package==version'}
                                style={{padding: '0px 0px 6px 0px'}}
                            />
                        </div>
                    </StyledAccordionDetails>
                </StyledAccordion>
                <StyledAccordion
                    variant={'outlined'}
                    expanded={this.state.filesExpanded}
                    style={{background: 'var(--jp-layout-color1)'}}
                >
                    <StyledAccordionSummary style={{cursor: 'default'}}>
                        <SubHeader title='Files' />
                        {(this.state.problemFiles.length > 0 || this.state.problemDataConnectors.length > 0) && <WarningRounded fontSize={'small'} style={{color: this.props.theme.palette.error.main, marginTop: '4px'}} />}
                        <span style={{
                            margin: 'auto 15px',
                            flexGrow: 1,
                            textAlign: 'end',
                            opacity: this.state.filesExpanded ? 0 : 0.5,
                            transitionDuration: '217ms',
                            whiteSpace: 'nowrap',
                            fontSize: '12px',
                            fontStyle: 'italic',
                        }}>
                            {files.length > 0 && (files.length + ' upload' + (files.length > 1 ? 's' : ''))}{files.length > 0 && dataConnectors.length > 0 ? ', ' : ''}{dataConnectors.length > 0 && (dataConnectors.length + ' connector' + (dataConnectors.length > 1 ? 's' : ''))}
                        </span>
                        <IconButton
                            onClick={() => this.safeSetState({filesExpanded: !this.state.filesExpanded})}
                            style={{padding: '0px', marginRight: '-3px', width: '30px'}}
                        >
                            <ExpandMore />
                        </IconButton>
                    </StyledAccordionSummary>
                    <StyledAccordionDetails>
                        <div style={{display: 'inline-flex', width: '100%'}}>
                            <AddFilesPopup onFilesAdded={async (metadatas: FileMetadata[]) => {
                                for (let fileModel of metadatas) {
                                    // Don't try to add the same file/directory more than once
                                    if (this.pathHasError(fileModel.path)) continue;
                                    const tracker = Global.metadata
                                    const optumi = tracker.getMetadata()
                                    var files = optumi.config.upload.files
                                    if (fileModel.type != 'directory') {
                                        files.push(new FileUploadConfig({
                                            path: fileModel.path,
                                            type: fileModel.type,
                                            mimetype: fileModel.mimetype,
                                            files: [fileModel.path]
                                        }))
                                    } else {
                                        files.push(new FileUploadConfig({
                                            path: fileModel.path,
                                            type: fileModel.type,
                                            mimetype: fileModel.mimetype,
                                            files: (await FileServerUtils.getRecursiveTree(fileModel.path))
                                        }))
                                    }
                                    tracker.setMetadata(optumi)
                                }
                            }} />
                            <AddDataConnectorsPopup openUserDialogTo={this.props.openUserDialogTo}
								onDataConnectorsAdded={async (metadatas: DataConnectorMetadata[]) => {
                                	for (let dataConnectorModel of metadatas) {
                                    	// Don't try to add the same file/directory more than once
                                    	if (this.nameHasError(dataConnectorModel.name)) continue;
                                    	const tracker = Global.metadata
                                    	const optumi = tracker.getMetadata()
                                    	var dataConnectors = optumi.config.upload.dataConnectors
                                    	dataConnectors.push(new DataConnectorUploadConfig({
                                        	name: dataConnectorModel.name,
                                        	dataService: dataConnectorModel.dataService,
                                    	}))
                                    	tracker.setMetadata(optumi)
                                	}
                            	}
							} />
                        </div>
                        {files.length == 0 && dataConnectors.length == 0 ? (
                            <div
                                style={{
                                fontSize: '12px',
                                lineHeight: '14px',
                                padding: '3px 6px 3px 6px',
                            }}>
                                None
                            </div>
                        ) : (
                            <>
                                {files.map(
                                    (value: FileUploadConfig) => (
                                        <ResourceFile
                                            key={value.path}
                                            file={value}
                                            handleFileDelete={() => {
                                                const tracker: OptumiMetadataTracker = Global.metadata;
                                                const optumi = tracker.getMetadata();
                                                const files = optumi.config.upload.files
                                                for (var i = 0; i < files.length; i++) {
                                                    if (files[i].path === value.path) {
                                                        files.splice(i, 1)
                                                        break
                                                    }
                                                }
                                                // optumi.upload.files = (optumi.upload.files as UploadVarMetadata[]).filter(x => x.path !== (event.currentTarget as HTMLButtonElement).id.replace('-delete', ''));
                                                tracker.setMetadata(optumi);
                                                if (this.state.problemFiles.includes(value.path)) this.safeSetState({ problemFiles: this.state.problemFiles.filter(x => x != value.path) });
                                            }}
                                            noLongerExists={this.state.problemFiles.includes(value.path)}
                                        />
                                    )
                                )}
                                {dataConnectors.map(
                                    (value: DataConnectorUploadConfig) => (
                                        <ResourceDataConnector
                                            key={value.name}
                                            dataConnector={value}
                                            handleFileDelete={() => {
                                                const tracker: OptumiMetadataTracker = Global.metadata;
                                                const optumi = tracker.getMetadata();
                                                const dataConnectors = optumi.config.upload.dataConnectors
                                                for (var i = 0; i < dataConnectors.length; i++) {
                                                    if (dataConnectors[i].name === value.name) {
                                                        dataConnectors.splice(i, 1)
                                                        break
                                                    }
                                                }
                                                // optumi.upload.files = (optumi.upload.files as UploadVarMetadata[]).filter(x => x.path !== (event.currentTarget as HTMLButtonElement).id.replace('-delete', ''));
                                                tracker.setMetadata(optumi);
                                                if (this.state.problemDataConnectors.includes(value.name)) this.safeSetState({ problemDataConnectors: this.state.problemDataConnectors.filter(x => x != value.name) });
                                            }}
                                            noLongerExists={this.state.problemDataConnectors.includes(value.name)}
                                        />
                                    )
                                )}
                            </>
                        )}
                    </StyledAccordionDetails>
                </StyledAccordion>
                <StyledAccordionSummary style={{cursor: 'default'}}>
                    <SubHeader title='Notifications' />
                    <span style={{
                        margin: 'auto 15px',
                        flexGrow: 1,
                        textAlign: 'end',
                        opacity: 0.5,
                        transitionDuration: '217ms',
                        whiteSpace: 'nowrap',
                        fontSize: '12px',
                        fontStyle: 'italic',
                    }}>
                        {(() => {
                            let numEnabled = 0
							const config = Global.metadata.getMetadata().config
                            if (!config.interactive) {
                                const notifications = config.notifications;
                                if (notifications.jobStartedSMSEnabled) numEnabled++;
                                if (notifications.jobFailedSMSEnabled || notifications.jobCompletedSMSEnabled) numEnabled++;
                                // TODO:JJ This currently does not refresh automatically when Global.user.notificationsEnabled changes, and I wasn't sure how to quickly do this.
                                if (Global.user.notificationsEnabled && numEnabled > 0) {
                                    return numEnabled + ' enabled'
                                }
                            }
                        })()}
                    </span>
                    <NotificationsPopup disabled={Global.metadata.getMetadata().config.interactive} openUserDialogTo={this.props.openUserDialogTo} />
                </StyledAccordionSummary>
            </div>
        )
    }

    private refreshFiles = async () => {
        if (this.refreshingFiles) {
            if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
            setTimeout(this.refreshFiles, 60000);
            const optumi = Global.metadata.getMetadata().config;
            const files = optumi.upload.files;
            for (var file of files) {
                if (!this.refreshingFiles) break;
                if (!this.state.problemFiles.includes(file.path)) {
                    const barr = await FileServerUtils.checkIfPathExists(file.path);
                    if (!barr[0]) {
                        this.safeSetState({ problemFiles: this.state.problemFiles.concat([file.path]) });
                    }
                }
            }
        }
    }

    private refreshDataConnectors = async () => {
        if (this.refreshingDataConnectors) {
            if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
            setTimeout(this.refreshDataConnectors, 60000);
            const optumi = Global.metadata.getMetadata().config;
            const dataConnectors = optumi.upload.dataConnectors;
            
            const settings = ServerConnection.makeSettings();
            const url = settings.baseUrl + "optumi/get-data-connectors";
            const dataConnectorsFromController: DataConnectorMetadata[] = await (ServerConnection.makeRequest(url, {}, settings).then(response => {
                if (response.status !== 200) throw new ServerConnection.ResponseError(response);
                return response.json();
            }).then((json: any) => json.connectors));

            for (var dataConnector of dataConnectors) {
                if (!this.refreshingDataConnectors) break;
                if (!this.state.problemDataConnectors.includes(dataConnector.name)) {
                    const exists = dataConnectorsFromController.map(x => x.name).includes(dataConnector.name);
                    if (!exists) {
                        this.safeSetState({ problemDataConnectors: this.state.problemDataConnectors.concat([dataConnector.name]) });
                    }
                }
            }
        }
    }

    private handleMetadataChange = () => {this.forceUpdate()}
	private handleLabShellChange = () => {this.forceUpdate()}

	// Will be called automatically when the component is mounted
	public componentDidMount = () => {
        this._isMounted = true
        this.refreshingFiles = true;
        this.refreshingDataConnectors = true;
        this.refreshFiles();
        this.refreshDataConnectors();
		Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
		Global.labShell.currentChanged.connect(this.handleLabShellChange);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
        Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
        Global.labShell.currentChanged.disconnect(this.handleLabShellChange);
        this.refreshingFiles = false;
        this.refreshingDataConnectors = false;
        this._isMounted = false
    }

    private safeSetState = (map: any) => {
		if (this._isMounted) {
			let update = false
			try {
				for (const key of Object.keys(map)) {
					if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
						update = true
						break
					}
				}
			} catch (error) {
				update = true
			}
			if (update) {
				if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
				this.setState(map)
			} else {
				if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
			}
		}
	}
    
    public shouldComponentUpdate = (nextProps: IProps, nextState: IState): boolean => {
        try {
            if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
            if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
            if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
            return false;
        } catch (error) {
            return true;
        }
    }
}
const ThemedFilesPanel = withTheme(FilesPanel)
export { ThemedFilesPanel as FilesPanel }

interface RFProps {
    file: FileUploadConfig,
    handleFileDelete: () => void,
    noLongerExists?: boolean,
}

interface RFState {
    hovering: boolean,
}

class ResourceFile extends React.Component<RFProps, RFState> {
    _isMounted: boolean = false

    constructor(props: RFProps) {
        super(props)
        this.state = {
            hovering: false,
        }
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <div
                style={{display: 'flex', width: '100%', position: 'relative'}}
                onMouseOver={() => {
                    this.safeSetState({hovering: true})
                }}
                onMouseOut={() => {
                    this.safeSetState({hovering: false})
                }}
            >
                <div style={{
                    position: 'absolute',
                    right: '-16px',
                    display: 'inline-flex',
                    background: 'var(--jp-layout-color1)',
                    opacity: this.state.hovering ? '1' : '0',
                    transition: easeAnimation,
                }}>
                    <IconButton onClick={this.props.handleFileDelete} style={{
                        width: '22px',
                        height: '22px',
                        padding: '0px',
                        position: 'relative',
                        display: 'inline-block',
                    }}>
                        <CloseIcon style={{position: 'relative', width: '16px', height: '16px'}} />
                    </IconButton>
                </div>
                <div
                    style={{
                        width: '100%',
                        fontSize: '12px',
                        lineHeight: '14px',
                        padding: '3px 6px 3px 6px',
                        display: 'inline-flex'
                    }}
                >   
                    <DirListingItemIcon
                        fileType={this.props.file.type}
                        mimetype={this.props.file.mimetype}
                    />
                    <div
                        style={{
                            margin: 'auto 0px',
                            overflow: 'hidden', 
                            color: this.props.noLongerExists ? '#f48f8d' : ''
                        }}
                        title={
                            (this.props.file.path.includes('/') ? (
`Name: ${this.props.file.path.split('/').pop()}
Path: ${this.props.file.path.replace(/\/[^\/]*$/, '')}`
                            ) : (
`Name: ${this.props.file.path.split('/').pop()}`
                            ))
                        }
                    >
                        <div style={{
                            direction: 'rtl',
                            overflow: 'hidden', 
                            textOverflow: 'ellipsis', 
                            whiteSpace: 'nowrap',
                        }}>
                            {this.props.file.path + (this.props.noLongerExists ? ' (no longer exists)' : '')}
                        </div>
                    </div>
                </div>
            </div>
        )
    }

    public componentDidMount = () => {
        this._isMounted = true
    }

    public componentWillUnmount = () => {
        this._isMounted = false
    }

    private safeSetState = (map: any) => {
		if (this._isMounted) {
			let update = false
			try {
				for (const key of Object.keys(map)) {
					if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
						update = true
						break
					}
				}
			} catch (error) {
				update = true
			}
			if (update) {
				if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
				this.setState(map)
			} else {
				if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
			}
		}
	}

    public shouldComponentUpdate = (nextProps: RFProps, nextState: RFState): boolean => {
        try {
            if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
            if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
            if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
            return false;
        } catch (error) {
            return true;
        }
    }
}

interface RDCProps {
    dataConnector: DataConnectorUploadConfig,
    handleFileDelete: () => void,
    noLongerExists?: boolean,
}

interface RDCState {
    hovering: boolean,
}

class ResourceDataConnector extends React.Component<RDCProps, RDCState> {
    _isMounted: boolean = false

    constructor(props: RDCProps) {
        super(props)
        this.state = {
            hovering: false,
        }
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <div
                style={{display: 'flex', width: '100%', position: 'relative'}}
                onMouseOver={() => {
                    this.safeSetState({hovering: true})
                }}
                onMouseOut={() => {
                    this.safeSetState({hovering: false})
                }}
            >
                <div style={{
                    position: 'absolute',
                    right: '-16px',
                    display: 'inline-flex',
                    background: 'var(--jp-layout-color1)',
                    opacity: this.state.hovering ? '1' : '0',
                    transition: easeAnimation,
                }}>
                    <IconButton onClick={this.props.handleFileDelete} style={{
                        width: '22px',
                        height: '22px',
                        padding: '0px',
                        position: 'relative',
                        display: 'inline-block',
                    }}>
                        <CloseIcon style={{position: 'relative', width: '16px', height: '16px'}} />
                    </IconButton>
                </div>
                <div
                    style={{
                        width: '100%',
                        fontSize: '12px',
                        lineHeight: '14px',
                        padding: '3px 6px 3px 6px',
                        display: 'inline-flex'
                    }}
                >   
                    <DataConnectorDirListingItemIcon
                        dataService={this.props.dataConnector.dataService}
                    />
                    <div
                        style={{
                            margin: 'auto 0px',
                            overflow: 'hidden', 
                            textOverflow: 'ellipsis', 
                            whiteSpace: 'nowrap',
                            direction: 'rtl',
                            color: this.props.noLongerExists ? '#f48f8d' : ''
                        }}
                    >
                        {this.props.dataConnector.name + (this.props.noLongerExists ? ' (no longer exists)' : '')}
                    </div>
                </div>
            </div>
        )
    }

    public componentDidMount = () => {
        this._isMounted = true
    }

    public componentWillUnmount = () => {
        this._isMounted = false
    }

    private safeSetState = (map: any) => {
		if (this._isMounted) {
			let update = false
			try {
				for (const key of Object.keys(map)) {
					if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
						update = true
						break
					}
				}
			} catch (error) {
				update = true
			}
			if (update) {
				if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
				this.setState(map)
			} else {
				if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
			}
		}
	}

    public shouldComponentUpdate = (nextProps: RDCProps, nextState: RDCState): boolean => {
        try {
            if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
            if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
            if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
            return false;
        } catch (error) {
            return true;
        }
    }
}
