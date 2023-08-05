import React from 'react';
import { Recording, Sorting, WorkspaceRouteDispatch } from '../../pluginInterface';
import { SortingCurationWorkspaceAction } from '../../pluginInterface/workspaceReducer';
interface Props {
    sorting: Sorting;
    recording: Recording;
    width: number;
    height: number;
    workspaceRouteDispatch: WorkspaceRouteDispatch;
    readOnly: boolean;
    curationDispatch: (a: SortingCurationWorkspaceAction) => void;
}
declare const SortingView: React.FunctionComponent<Props>;
export default SortingView;
