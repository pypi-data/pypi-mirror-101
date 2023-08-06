import { FunctionComponent } from 'react';
import { Recording, Sorting, SortingCuration, SortingSelection, SortingSelectionDispatch } from "../../pluginInterface";
import { SpikeAmplitudesData } from './useSpikeAmplitudesData';
declare type Props = {
    spikeAmplitudesData: SpikeAmplitudesData;
    recording: Recording;
    sorting: Sorting;
    unitIds: number[];
    width: number;
    height: number;
    selection: SortingSelection;
    selectionDispatch: SortingSelectionDispatch;
    curation: SortingCuration;
};
declare const SpikeAmplitudesTimeWidget: FunctionComponent<Props>;
export default SpikeAmplitudesTimeWidget;
