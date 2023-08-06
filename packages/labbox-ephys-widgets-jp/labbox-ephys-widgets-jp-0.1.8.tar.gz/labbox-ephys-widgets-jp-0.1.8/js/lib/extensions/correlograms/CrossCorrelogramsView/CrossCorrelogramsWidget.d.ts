import { FunctionComponent } from 'react';
import { Sorting, SortingCuration, SortingSelection, SortingSelectionDispatch } from "../../pluginInterface";
declare type Props = {
    sorting: Sorting;
    selection: SortingSelection;
    curation: SortingCuration;
    selectionDispatch: SortingSelectionDispatch;
    unitIds: number[];
    width: number;
    height: number;
};
declare const CrossCorrelogramsWidget: FunctionComponent<Props>;
export default CrossCorrelogramsWidget;
