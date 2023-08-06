import { Modal } from '@material-ui/core';
import React, { useCallback, useEffect, useState } from 'react';
import { useWorkspaceViewPlugins } from '../../pluginInterface';
import ApplicationBar from './ApplicationBar';
import HitherJobMonitorWindow from './HitherJobMonitorWindow';
import SettingsWindow from './SettingsWindow';
// Thanks: https://stackoverflow.com/questions/36862334/get-viewport-window-height-in-reactjs
function getWindowDimensions() {
    const { innerWidth: width, innerHeight: height } = window;
    return {
        width,
        height
    };
}
function useWindowDimensions() {
    const [windowDimensions, setWindowDimensions] = useState(getWindowDimensions());
    useEffect(() => {
        function handleResize() {
            setWindowDimensions(getWindowDimensions());
        }
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);
    return windowDimensions;
}
const MainWindow = ({ workspace, workspaceDispatch, workspaceRoute, workspaceRouteDispatch, version, width, height }) => {
    const { width: width2, height: height2 } = useWindowDimensions();
    const appBarHeight = 52; // hard-coded for now - must agree with theme
    const H = (height || height2) - appBarHeight - 2;
    const hMargin = 0;
    const W = (width || width2) - hMargin * 2 - 2;
    const workspaceViewPlugin = useWorkspaceViewPlugins().filter(p => (p.name === 'WorkspaceView'))[0];
    if (!workspaceViewPlugin)
        throw Error('Unable to find workspace view plugin');
    const [settingsVisible, setSettingsVisible] = useState(false);
    const [jobMonitorVisible, setJobMonitorVisible] = useState(false);
    const handleOpenSettings = useCallback(() => {
        setSettingsVisible(true);
    }, []);
    const handleOpenJobMonitor = useCallback(() => {
        setJobMonitorVisible(true);
    }, []);
    const handleCloseSettings = useCallback(() => {
        setSettingsVisible(false);
    }, []);
    const handleCloseJobMonitor = useCallback(() => {
        setJobMonitorVisible(false);
    }, []);
    return (React.createElement("div", { style: { margin: 0 } },
        React.createElement(ApplicationBar, { onOpenSettings: handleOpenSettings, onOpenJobMonitor: handleOpenJobMonitor, workspaceRouteDispatch: workspaceRouteDispatch }),
        React.createElement("div", { style: { position: 'absolute', top: appBarHeight } },
            React.createElement(workspaceViewPlugin.component, { width: W, height: H, workspace: workspace, workspaceDispatch: workspaceDispatch, workspaceRoute: workspaceRoute, workspaceRouteDispatch: workspaceRouteDispatch })),
        React.createElement(Modal, { open: settingsVisible, onClose: handleCloseSettings, style: { zIndex: 9999 } },
            React.createElement("span", null,
                React.createElement(SettingsWindow, { workspace: workspace, workspaceUri: workspaceRoute.workspaceUri, version: version }))),
        React.createElement(Modal, { open: jobMonitorVisible, onClose: handleCloseJobMonitor, style: { zIndex: 9999 } },
            React.createElement("span", null,
                React.createElement(HitherJobMonitorWindow, null)))));
};
export default MainWindow;
//# sourceMappingURL=MainWindow.js.map