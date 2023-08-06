import { makeStyles } from '@material-ui/core/styles';
import React, { useCallback, useState } from 'react';
import { useMonitorHitherJobs } from './HitherJobMonitorControl';
import HitherJobMonitorJobView from './HitherJobMonitorJobView';
import HitherJobMonitorTable from './HitherJobMonitorTable';
const useStyles = makeStyles((theme) => ({
    paper: {
        left: 100,
        top: 100,
        right: 100,
        bottom: 100,
        position: 'absolute',
        backgroundColor: theme.palette.background.paper,
        border: '2px solid #000',
        boxShadow: theme.shadows[5],
        padding: theme.spacing(2, 4, 3),
        overflow: 'auto'
    },
}));
const HitherJobMonitorWindow = () => {
    const classes = useStyles();
    const { allJobs } = useMonitorHitherJobs();
    const [currentJob, setCurrentJob] = useState(null);
    const handleViewJob = useCallback((job) => {
        setCurrentJob(job);
    }, []);
    const handleCancelJob = useCallback(() => {
    }, []);
    const handleBack = useCallback(() => {
        setCurrentJob(null);
    }, []);
    return (React.createElement("div", { className: classes.paper, style: { zIndex: 9999 } },
        React.createElement("h2", null, "Job Monitor"),
        currentJob ? (React.createElement(HitherJobMonitorJobView, { job: currentJob, onBack: handleBack })) : (React.createElement(HitherJobMonitorTable, { jobs: allJobs, onViewJob: handleViewJob, onCancelJob: handleCancelJob }))));
};
export default HitherJobMonitorWindow;
//# sourceMappingURL=HitherJobMonitorWindow.js.map