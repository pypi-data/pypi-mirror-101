/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { Input, withStyles } from '@material-ui/core';
import * as React from 'react';
import { Global } from '../../Global';

const StyledInput = withStyles({
    root: {
        fontSize: 'var(--jp-ui-font-size1)', 
        lineHeight: '1', 
        fontWeight: 'normal', 
        width: '200px',
    },
    input: {
        padding: '2px 0px',
    },
    underline: {
        '&:hover:before': {
            borderBottom: '1px solid rgba(0, 0, 0, 0.87) !important',
        },
        '&::before': {
            borderBottom: 'none',
        },
    },
})(Input);

interface IProps {
    getValue: () => string
    saveValue: (value: string) => void
    placeholder: string
    style?: React.CSSProperties,
}

interface IState {
    value: string
    editing: boolean
}

export class AnnotationInput extends React.Component<IProps, IState> {
    private _isMounted = false;
    textField: React.RefObject<HTMLInputElement>

    constructor(props: IProps) {
        super(props);
        this.textField = React.createRef();
        this.state = {
            value: this.props.getValue(),
            editing: false,
        }
    }
    
    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <>
                <StyledInput
                    inputRef={this.textField}
                    value={this.state.value}
                    onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                        const value = event.target.value;
                        this.safeSetState({ value: value })
                    }}
                    onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => {
                        if (e.key === 'Enter') {
                            this.textField.current.blur();
                        }
                    }}
                    onBlur={() => this.props.saveValue(this.state.value)}
                    placeholder={this.props.placeholder}
                />
            </>
        )
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
