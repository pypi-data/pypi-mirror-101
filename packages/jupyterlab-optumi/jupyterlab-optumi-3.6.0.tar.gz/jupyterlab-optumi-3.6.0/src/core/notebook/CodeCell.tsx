/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import InputArea from './InputArea'
import OutputArea from './OutputArea'
import { Global } from '../../Global';

interface IProps {
    cell: any
    metadata: any
    renderInColor: boolean
}

interface IState {}

export default class CodeCell extends React.Component<IProps, IState> {

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <div className='p-Widget lm-Widget jp-Cell jp-CodeCell jp-Notebook-cell' onContextMenu={(e) => e.preventDefault()}>
                <InputArea cell={this.props.cell} metadata={this.props.metadata} renderInColor={this.props.renderInColor} />
                <OutputArea cell={this.props.cell} metadata={this.props.metadata} />
            </div>
        )
    }
}
