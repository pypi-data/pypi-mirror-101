import React from 'react';
import sizeMe from 'react-sizeme';
import { SortingCuration, SortingSelection, SortingSelectionDispatch } from '../../pluginInterface';
import { SortingCurationAction } from '../../pluginInterface/SortingCuration';
declare const _default: React.ComponentType<{
    selection: SortingSelection;
    selectionDispatch: SortingSelectionDispatch;
    curation: SortingCuration;
    curationDispatch: (a: SortingCurationAction) => void;
    sortingId: string;
} & sizeMe.WithSizeProps>;
export default _default;
