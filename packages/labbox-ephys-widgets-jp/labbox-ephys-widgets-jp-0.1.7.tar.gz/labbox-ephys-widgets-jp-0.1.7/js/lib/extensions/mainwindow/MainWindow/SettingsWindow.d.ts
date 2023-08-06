import { FunctionComponent } from 'react';
import { WorkspaceState } from '../../pluginInterface/workspaceReducer';
declare type Props = {
    workspace: WorkspaceState;
    workspaceUri: string | undefined;
    version: string;
};
declare const SettingsWindow: FunctionComponent<Props>;
export default SettingsWindow;
