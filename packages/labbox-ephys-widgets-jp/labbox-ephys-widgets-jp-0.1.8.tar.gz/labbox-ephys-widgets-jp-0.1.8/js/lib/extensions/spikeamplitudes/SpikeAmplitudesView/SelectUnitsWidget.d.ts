import { FunctionComponent } from 'react';
import { Sorting, SortingCuration, SortingSelection, SortingSelectionDispatch } from "../../pluginInterface";
declare type Props = {
    sorting: Sorting;
    selection: SortingSelection;
    selectionDispatch: SortingSelectionDispatch;
    curation: SortingCuration;
};
declare const SelectUnitsWidget: FunctionComponent<Props>;
export default SelectUnitsWidget;
