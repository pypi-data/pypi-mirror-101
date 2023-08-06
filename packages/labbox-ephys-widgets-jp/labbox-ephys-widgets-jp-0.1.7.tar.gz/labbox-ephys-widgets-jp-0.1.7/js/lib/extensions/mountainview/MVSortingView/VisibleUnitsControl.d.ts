import { FunctionComponent } from 'react';
import { Recording, Sorting, SortingCuration, SortingSelection, SortingSelectionDispatch } from "../../pluginInterface";
declare type Props = {
    sorting: Sorting;
    recording: Recording;
    selection: SortingSelection;
    selectionDispatch: SortingSelectionDispatch;
    curation: SortingCuration;
};
declare const VisibleUnitsControl: FunctionComponent<Props>;
export default VisibleUnitsControl;
