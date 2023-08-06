import { HitherContext } from 'labbox';
import React, { useContext, useEffect, useState } from 'react';
import Hyperlink from '../../common/Hyperlink';
export const useMonitorHitherJobs = () => {
    const [hitherJobs, setHitherJobs] = useState([]);
    const hither = useContext(HitherContext);
    useEffect(() => {
        // this should only get called once
        // (hither should not change, but if it does we might have a problem here)
        const timer1 = setInterval(() => {
            const hj = hither.getHitherJobs();
            setHitherJobs(hj);
        }, 1000);
        return () => {
            clearInterval(timer1);
        };
    }, [hither]);
    return {
        pendingJobs: hitherJobs.filter(j => (j.status === 'pending')),
        runningJobs: hitherJobs.filter(j => (j.status === 'running')),
        finishedJobs: hitherJobs.filter(j => (j.status === 'finished')),
        erroredJobs: hitherJobs.filter(j => (j.status === 'error')),
        allJobs: hitherJobs
    };
};
const HitherJobMonitorControl = ({ onClick }) => {
    const { pendingJobs, runningJobs, finishedJobs, erroredJobs } = useMonitorHitherJobs();
    const numPending = pendingJobs.length;
    const numRunning = runningJobs.length;
    const numFinished = finishedJobs.length;
    const numErrored = erroredJobs.length;
    const title = `Jobs: ${numPending} pending | ${numRunning} running | ${numFinished} finished | ${numErrored} errored`;
    const errored = numErrored > 0 ? (React.createElement("span", null,
        ":",
        React.createElement("span", { style: { color: 'pink' } }, numErrored))) : React.createElement("span", null);
    return (React.createElement(Hyperlink, { onClick: onClick, color: "white" },
        React.createElement("span", { title: title, style: { fontFamily: "courier" } },
            numPending,
            ":",
            numRunning,
            ":",
            numFinished,
            errored)));
};
export default HitherJobMonitorControl;
//# sourceMappingURL=HitherJobMonitorControl.js.map