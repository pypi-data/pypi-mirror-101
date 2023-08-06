import React from 'react';
import { Recording, Sorting, WorkspaceRoute, WorkspaceRouteDispatch } from '../../pluginInterface';
interface Props {
    sorting: Sorting;
    recording: Recording;
    width: number;
    height: number;
    workspaceRoute: WorkspaceRoute;
    workspaceRouteDispatch: WorkspaceRouteDispatch;
    readOnly: boolean;
}
declare const SortingView: React.FunctionComponent<Props>;
export default SortingView;
