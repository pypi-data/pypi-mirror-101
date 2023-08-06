import { FunctionComponent } from 'react';
import { Sorting, SortingCuration, SortingSelection, SortingSelectionDispatch, SortingUnitMetricPlugin } from "../../pluginInterface";
import '../unitstable.css';
interface Props {
    sortingUnitMetrics?: SortingUnitMetricPlugin[];
    units: number[];
    metrics?: {
        [key: string]: {
            data: {
                [key: string]: any;
            };
            error: string | null;
        };
    };
    selection: SortingSelection;
    selectionDispatch: SortingSelectionDispatch;
    sorting: Sorting;
    curation: SortingCuration;
    height?: number;
}
declare const UnitsTable: FunctionComponent<Props>;
export default UnitsTable;
