/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { SubHeader } from '../../../core';
import { Global } from '../../../Global';
import { Expertise } from '../../../models/OptumiConfig';
import { OptumiMetadataTracker } from '../../../models/OptumiMetadataTracker';
import ExtraInfo from '../../../utils/ExtraInfo';

import { OutlinedResourceRadio } from '../OutlinedResourceRadio';

interface IProps {
    style?: React.CSSProperties,
}

interface IState {}

export class Basic extends React.Component<IProps, IState> {

    private getValue(): string {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
		if (optumi.config.graphics.required == true) return "GPU";
        if (optumi.config.compute.required == true) return "CPU";
        if (optumi.config.memory.required == true) return "RAM";
        if (optumi.config.storage.required == true) return "DSK";
        return "CPU";
	}

	private saveValue(value: string) {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
        optumi.config.graphics.required = value == "GPU" ? true : false;
        optumi.config.compute.required = value == "CPU" ? true : false;
        optumi.config.memory.required = value == "RAM" ? true : false;
        optumi.config.storage.required = value == "DSK" ? true : false;
        tracker.setMetadata(optumi);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const value = this.getValue();
        return (
            <>
                <SubHeader title='Resource Selection'/>
                <div
                    style={{
                        alignItems: 'center',
                        display: 'inline-flex',
                        width: '100%',
                    }}
                >
                    <ExtraInfo reminder='Optimize for GPU'>
                        <OutlinedResourceRadio label={"GPU"} hexColor={'#ffba7d'} selected={value == "GPU"} handleClick={() => this.saveValue("GPU")}/>
                    </ExtraInfo>
                    <ExtraInfo reminder='Optimize for CPU'>
                        <OutlinedResourceRadio label={"CPU"} hexColor={'#f48f8d'} selected={value == "CPU"} handleClick={() => this.saveValue("CPU")}/>
                    </ExtraInfo>
                    <ExtraInfo reminder='Optimize for RAM'>
                        <OutlinedResourceRadio label={"RAM"} hexColor={'#afaab0'} selected={value == "RAM"} handleClick={() => this.saveValue("RAM")}/>
                    </ExtraInfo>
                </div>
            </>
        )
    }

    private handleMetadataChange = () => { this.forceUpdate() }

    // Will be called automatically when the component is mounted
	public componentDidMount = () => {
        Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);

        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        // Ser all resource levels to basic
        optumi.config.graphics.expertise = Expertise.BASIC;
        optumi.config.compute.expertise = Expertise.BASIC;
        optumi.config.memory.expertise = Expertise.BASIC;
        optumi.config.storage.expertise = Expertise.BASIC;
        // Make sure only one required flag is set to true
        if (optumi.config.graphics.required) {
            optumi.config.compute.required = false;
            optumi.config.memory.required = false;
            optumi.config.storage.required = false
        } else if (optumi.config.compute.required) {
            optumi.config.graphics.required = false;
            optumi.config.memory.required = false;
            optumi.config.storage.required = false
        } else if (optumi.config.memory.required) {
            optumi.config.graphics.required = false;
            optumi.config.compute.required = false;
            optumi.config.storage.required = false
        } else {    // By default we will set compute to required
            optumi.config.graphics.required = false;
            optumi.config.compute.required = true;
            optumi.config.memory.required = false;
            optumi.config.storage.required = false
        }
        tracker.setMetadata(optumi);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
        Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
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
