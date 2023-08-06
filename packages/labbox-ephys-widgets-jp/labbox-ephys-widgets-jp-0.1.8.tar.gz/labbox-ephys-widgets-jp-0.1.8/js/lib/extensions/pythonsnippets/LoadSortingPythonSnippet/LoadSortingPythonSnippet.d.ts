import React from 'react';
import sizeMe from 'react-sizeme';
declare const _default: React.ComponentType<{
    recording: import("../../pluginInterface").Recording;
    sorting: import("../../pluginInterface").Sorting;
    height: number;
    width: number;
    readOnly: boolean | null;
    selection: import("../../pluginInterface").SortingSelection;
    selectionDispatch: (a: import("../../pluginInterface").SortingSelectionAction) => void;
    curation: import("../../pluginInterface").SortingCuration;
    sortingInfo: import("../../pluginInterface").SortingInfo;
    recordingInfo: import("../../pluginInterface").RecordingInfo;
    curationDispatch: (action: import("../../pluginInterface/SortingCuration").SortingCurationAction) => void;
    calculationPool: import("labbox").CalculationPool;
} & sizeMe.WithSizeProps>;
export default _default;
