import { Recording } from "./Recording";
import { Sorting } from "./Sorting";
import { SortingCuration, SortingCurationAction } from "./SortingCuration";
export declare type WorkspaceState = {
    recordings: Recording[];
    sortings: Sorting[];
};
declare type AddRecordingWorkspaceAction = {
    type: 'ADD_RECORDING';
    recording: Recording;
};
declare type DeleteRecordingsWorkspaceAction = {
    type: 'DELETE_RECORDINGS';
    recordingIds: string[];
};
declare type AddSortingsWorkspaceAction = {
    type: 'ADD_SORTING';
    sorting: Sorting;
};
declare type DeleteSortingsWorkspaceAction = {
    type: 'DELETE_SORTINGS';
    sortingIds: string[];
};
declare type DeleteSortingsForRecordingsWorkspaceAction = {
    type: 'DELETE_SORTINGS_FOR_RECORDINGS';
    recordingIds: string[];
};
export interface SetUnitMetricsForSortingWorkspaceAction {
    type: 'SET_UNIT_METRICS_FOR_SORTING';
    unitMetricsForSorting: {
        sortingId: string;
        metricsUri: string;
    };
}
export declare type WorkspaceAction = AddRecordingWorkspaceAction | DeleteRecordingsWorkspaceAction | AddSortingsWorkspaceAction | DeleteSortingsWorkspaceAction | DeleteSortingsForRecordingsWorkspaceAction | SetUnitMetricsForSortingWorkspaceAction;
export declare const sortingCurationReducer: (state: SortingCuration, action: SortingCurationAction) => SortingCuration;
declare const workspaceReducer: (s: WorkspaceState, a: WorkspaceAction) => WorkspaceState;
export declare type WorkspaceDispatch = (a: WorkspaceAction) => void;
export default workspaceReducer;
