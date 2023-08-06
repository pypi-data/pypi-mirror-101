export declare type SortingCuration = {
    labelsByUnit?: {
        [key: string]: string[];
    };
    labelChoices?: string[];
    mergeGroups?: (number[])[];
};
export interface AddUnitLabelCurationAction {
    type: 'ADD_UNIT_LABEL';
    unitId: number;
    label: string;
}
export interface RemoveUnitLabelCurationAction {
    type: 'REMOVE_UNIT_LABEL';
    unitId: number;
    label: string;
}
export interface MergeUnitsCurationAction {
    type: 'MERGE_UNITS';
    unitIds: number[];
}
export interface UnmergeUnitsCurationAction {
    type: 'UNMERGE_UNITS';
    unitIds: number[];
}
export interface SetCurationCurationAction {
    type: 'SET_CURATION';
    curation: SortingCuration;
}
export declare type SortingCurationAction = AddUnitLabelCurationAction | RemoveUnitLabelCurationAction | MergeUnitsCurationAction | UnmergeUnitsCurationAction | SetCurationCurationAction;
export declare type SortingCurationDispatch = (action: SortingCurationAction) => void;
export declare const mergeGroupForUnitId: (unitId: number, curation: SortingCuration | undefined) => number[];
export declare const applyMergesToUnit: (unitId: number, curation: SortingCuration | undefined, applyMerges: boolean | undefined) => number | number[];
export declare const isMergeGroupRepresentative: (unitId: number, curation: SortingCuration | undefined) => boolean;
