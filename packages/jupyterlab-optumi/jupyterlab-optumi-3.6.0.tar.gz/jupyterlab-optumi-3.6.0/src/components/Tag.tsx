/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { withStyles, LinearProgress, Chip } from '@material-ui/core';
import { Global } from '../Global';
import { StatusColor } from './StatusWrapper';
import { CSSProperties } from '@material-ui/core/styles/withStyles';

interface IProps {
    id?: string
    label: string
    color?: string
    solid?: boolean
    showLoading?: boolean
    percentLoaded?: number
    icon? : JSX.Element;
    onMouseOver?: (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => void
    onMouseOut?: (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => void
    style?: CSSProperties
}

interface IState {}

const progressBorderSize: number = 1

export class Tag extends React.Component<IProps, IState> {

    // Do some extra work to avoid creating new styles every time this component renders
    PreviousStyledChip: any = null;
    PreviousStyledLinearProgress: any = null;

    StyledChip: any;
    StyledLinearProgress: any;

    public constructor(props: IProps) {
        super(props);
        this.StyledChip = this.getStyledChip();
        this.StyledLinearProgress = this.getStyledLinearProgress();
    }

    private getStyledChip = () => {
        return withStyles({
            root: {
                position: 'relative',
                bottom: '0px',
                margin: `${progressBorderSize}px`,
                height: '18px',
                backgroundColor: this.props.solid ? (this.props.color || StatusColor.DARK_GRAY) : 'var(--jp-layout-color2)',
                fontSize: 'var(--jp-ui-font-size1)',
                color: this.props.solid ? '#ffffff' : '',
            },
            label: {
                overflow: 'visible',
            }
        }) (Chip);
    }

    private getStyledLinearProgress = () => {
        return withStyles({
            root: {
                position: 'absolute',
                bottom: '0px',
                height: `${18 + (2 * progressBorderSize)}px`,
                borderRadius: `${(18 + (2 * progressBorderSize)) / 2}px`,
            },
            barColorPrimary: {
                backgroundColor: this.props.color || '#10A0F9',
            },
            colorPrimary: {
                backgroundColor: StatusColor.DARK_GRAY,
            },
        }) (LinearProgress);
    }

    private handleMouseOver = (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
        if (this.props.onMouseOver) this.props.onMouseOver(event);
    }

    private handleMouseOut = (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
        if (this.props.onMouseOut) this.props.onMouseOut(event);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <>
                {this.props.label != "" && this.props.label != undefined &&
                    <div
                        style={Object.assign({
                            position: 'relative',
                            margin: '3px',
                        }, this.props.style)}
                        onMouseOver={this.handleMouseOver}
                        onMouseOut={this.handleMouseOut}
                    >
                        {this.props.showLoading && (
                            this.props.percentLoaded === undefined ? (
                                <this.StyledLinearProgress
                                    style={{width: (Global.getStringWidth(this.props.label, '13px Roboto, Helvetica, Arial, sans-serif') + 14 + (2 * progressBorderSize)) + 'px'}}
                                />
                            ) : (
                                <this.StyledLinearProgress
                                    style={{width: (Global.getStringWidth(this.props.label, '13px Roboto, Helvetica, Arial, sans-serif') + 14 + (2 * progressBorderSize)) + 'px'}}
                                    variant='determinate'
                                    value={this.props.percentLoaded * 100}
                                />
                            )
                        )}
                        <this.StyledChip
                            key={this.props.label + this.props.color + this.props.icon}
                            id={this.props.id}
                            size='small'
                            label={this.props.label}
                            icon={this.props.icon}
                            style={{
                                border: !this.props.showLoading ? '1px solid ' + (this.props.color || StatusColor.DARK_GRAY) : '',
                                width: ((Global.getStringWidth(this.props.label, '13px Roboto, Helvetica, Arial, sans-serif') + 14) + (this.props.icon ? 14 : 0)) + 'px',
                            }}
                        />
                    </div>
                }
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
}
