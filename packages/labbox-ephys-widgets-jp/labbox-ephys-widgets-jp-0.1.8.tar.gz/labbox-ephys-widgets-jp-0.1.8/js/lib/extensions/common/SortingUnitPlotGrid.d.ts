import React, { FunctionComponent } from 'react';
import { Sorting, SortingCuration, SortingSelection, SortingSelectionDispatch } from "../pluginInterface";
declare type Props = {
    sorting: Sorting;
    selection: SortingSelection;
    curation: SortingCuration;
    selectionDispatch: SortingSelectionDispatch;
    unitComponent: (unitId: number) => React.ReactElement;
};
declare const SortingUnitPlotGrid: FunctionComponent<Props>;
export default SortingUnitPlotGrid;
