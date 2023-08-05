/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../Global';
import withStyles, { CSSProperties } from '@material-ui/core/styles/withStyles';
import { FormControl, FormHelperText, MenuItem, Select } from '@material-ui/core';

const StyledMenuItem = withStyles({
    root: {
        fontSize: 'var(--jp-ui-font-size1)',
        padding: '3px 3px 3px 6px',
        textAlign: 'start',
    }
}) (MenuItem)

interface IProps {
    style?: CSSProperties
    label?: string
    labelWidth?: string
    getValue: () => string
    saveValue: (value: string) => string | void
    values: {value: string, description: string}[]
    helperText?: string
    onFocus?: (event: React.FocusEvent<HTMLInputElement>) => void
    onBlur?: (event: React.FocusEvent<HTMLInputElement>) => void
    disabled?: boolean
}

interface IState {
    value: string
}

export class Dropdown extends React.Component<IProps, IState> {
    private _isMounted = false

    StyledSelect: any

    constructor(props: IProps) {
        super(props);
        this.state = {
            value: this.props.getValue(),
        }
        this.StyledSelect = this.getStyledSelect();
    }

    private getStyledSelect = () => {
        return withStyles({
            root: {
                fontSize: "var(--jp-ui-font-size1)",
                padding: '3px 3px 3px 6px',
                textAlign: 'start',
            },
            iconOutlined: {
                right: '0px'
            }
        }) (Select)
    }

    private handleValueChange = (event: React.ChangeEvent<{ value: unknown }>) => {
        const value = event.target.value as string
        this.safeSetState({value: value})
        this.props.saveValue(value);
    }
    
    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <div style={Object.assign({
                display: 'inline-flex',
                width: '100%',
                padding: '6px 0px',
                textAlign: 'center',
                justifyContent: 'center'
            }, this.props.style)}>
                {this.props.label && <div style={{
                    minWidth: this.props.labelWidth || '68px',
                    margin: '0px 12px',
                    lineHeight: '24px',
                }}>
                    {this.props.label}
                </div>}
                <FormControl
                    variant='outlined'
                    style={{width: '100%', margin: '2px 6px', height: this.props.helperText ? '32px' : '20px'}}
                >
                    <this.StyledSelect
                        value={this.state.value}
                        variant='outlined'
                        onChange={this.handleValueChange}
                        SelectDisplayProps={{style: {padding: '1px 20px 1px 6px'}}}
                        MenuProps={{MenuListProps: {style: {paddingTop: '6px', paddingBottom: '6px'}}}}
                        style={{width: '100%'}}
                        disabled={this.props.disabled}
                    >
                        {this.props.values.map(value =>
                            <StyledMenuItem key={value.value} value={value.value}>
                                {value.value + (value.description ? (': ' + value.description) : '')}
                            </StyledMenuItem>
                        )}
                    </this.StyledSelect>
                    {this.props.helperText && 
                        <FormHelperText style={{fontSize: '10px', lineHeight: '10px', margin: '4px 6px', whiteSpace: 'nowrap'}}>
                            {this.props.helperText}
                        </FormHelperText>
                    }
                </FormControl>
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
