/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import DataConnectorDirListingContent from './DataConnectorDirListingContent'
import { caretUpIcon, caretDownIcon } from '@jupyterlab/ui-components'
import { DataConnectorMetadata } from './DataConnectorBrowser'
import { Global } from '../../../Global';

interface IProps {
    dataConnectors: DataConnectorMetadata[]
    onOpen: (dataConnector: DataConnectorMetadata) => void
    getSelected?: (getSelected: () => DataConnectorMetadata[]) => void
    handleDelete?: (dataConnectorMetadata: DataConnectorMetadata) => void
}

interface IState {
    selected: 'name' | 'dataService'
    sorted: 'forward' | 'backward'
}

export default class DataConnectorDirListing extends React.Component<IProps, IState> {
    private _isMounted = false

    constructor(props: IProps) {
        super(props)
        this.state = {
            selected: 'name',
            sorted: 'forward',
        }
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const sort = (a: DataConnectorMetadata, b: DataConnectorMetadata) => {
            const sortDirection = (a: any, b: any): number => a.localeCompare(b) * (this.state.sorted === 'forward' ? 1 : -1);
            if (this.state.selected === 'name') {
                if (a.name === b.name) return a.dataService.localeCompare(b.dataService);
                return sortDirection(a.name, b.name)
            } else if (this.state.selected === 'dataService') {
                if (a.dataService === b.dataService) return a.name.localeCompare(b.name);
                return sortDirection(a.dataService, b.dataService)
            }
        }
        return (
            <div className='jp-DirListing jp-FileBrowser-listing' style={{overflow: 'hidden'}}>
                <div className='jp-DirListing-header'>
                    <div
                        className={'jp-DirListing-headerItem jp-id-data-service' + (this.state.selected === 'dataService' ? ' jp-mod-selected' : '')}
                        onClick={() => {
                            if (this.state.selected === 'dataService') {
                                this.safeSetState({sorted: this.state.sorted === 'forward' ? 'backward' : 'forward'})
                            } else {
                                this.safeSetState({selected: 'dataService', sorted: 'forward'})
                            }
                        }}
                        style={{flex: '0 0 210px', textAlign: 'left', padding: '4px 12px 2px 17px'}}
                    >
                        <span className='jp-DirListing-headerItemText'>
                            Data Service
                        </span>
                        {this.state.selected === 'dataService' && (
                            <span className='jp-DirListing-headerItemIcon' style={{float: 'right'}}>
                                {this.state.sorted === 'forward' ? (
                                    <caretUpIcon.react container={<></> as unknown as HTMLElement} />
                                ) : (
                                    <caretDownIcon.react container={<></> as unknown as HTMLElement} />
                                )}
                            </span>
                        )}
                    </div>
                    <div
                        className={'jp-DirListing-headerItem jp-id-name' + (this.state.selected === 'name' ? ' jp-mod-selected' : '')}
                        onClick={() => {
                            if (this.state.selected === 'name') {
                                this.safeSetState({sorted: this.state.sorted === 'forward' ? 'backward' : 'forward'})
                            } else {
                                this.safeSetState({selected: 'name', sorted: 'forward'})
                            }
                        }}
                        style={{padding: '4px 12px 2px 17px'}}
                    >
                        <span className='jp-DirListing-headerItemText'>
                            Name
                        </span>
                        {this.state.selected === 'name' && (
                            <span className='jp-DirListing-headerItemIcon' style={{float: 'right'}}>
                                {this.state.sorted === 'forward' ? (
                                    <caretUpIcon.react container={<></> as unknown as HTMLElement} />
                                ) : (
                                    <caretDownIcon.react container={<></> as unknown as HTMLElement} />
                                )}
                            </span>
                        )}
                    </div>
                </div>
                <div style={{marginBottom: '6px'}} />
                <DataConnectorDirListingContent
                    dataConnectors={this.props.dataConnectors}
                    handleDelete={this.props.handleDelete}
                    onOpen={this.props.onOpen}
                    sort={sort}
                    getSelected={this.props.getSelected}
                />
                <div style={{marginBottom: '6px'}} />
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
}