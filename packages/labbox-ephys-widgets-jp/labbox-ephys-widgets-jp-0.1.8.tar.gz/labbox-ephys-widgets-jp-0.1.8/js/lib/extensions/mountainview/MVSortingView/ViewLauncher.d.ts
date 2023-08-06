import { FunctionComponent } from 'react';
import { RecordingViewPlugin, SortingSelection, SortingUnitViewPlugin, SortingViewPlugin } from "../../pluginInterface";
export declare type ViewPluginType = 'RecordingView' | 'SortingView' | 'SortingUnitView';
declare type Props = {
    selection: SortingSelection;
    onLaunchSortingView: (plugin: SortingViewPlugin) => void;
    onLaunchRecordingView: (plugin: RecordingViewPlugin) => void;
    onLaunchSortingUnitView: (plugin: SortingUnitViewPlugin, unitId: number, label: string) => void;
    hasSorting: boolean;
};
declare const ViewLauncher: FunctionComponent<Props>;
export default ViewLauncher;
