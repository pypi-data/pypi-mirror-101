import NiceTable from "../../common/NiceTable";
import React, { useMemo } from "react";
import Hyperlink from "../../common/Hyperlink";
import { IconButton } from "@material-ui/core";
import { Delete } from "@material-ui/icons";
const HitherJobMonitorTable = ({ jobs, onViewJob, onCancelJob }) => {
    const columns = useMemo(() => ([
        {
            key: 'jobId',
            label: 'Job'
        },
        {
            key: 'functionName',
            label: 'Function'
        },
        {
            key: 'status',
            label: 'Status'
        },
        {
            key: 'started',
            label: 'Started'
        },
        {
            key: 'finished',
            label: 'Finished'
        },
        {
            key: 'message',
            label: 'Message'
        }
    ]), []);
    const sortedJobs = useMemo(() => ([...jobs].sort((j1, j2) => {
        if ((j1.status === 'running') && (j2.status !== 'running'))
            return -1;
        else if ((j2.status === 'running') && (j1.status !== 'running'))
            return 1;
        if ((j1.timestampStarted) && (j2.timestampStarted)) {
            if (j1.timestampStarted < j2.timestampStarted)
                return 1;
            else if (j2.timestampStarted < j1.timestampStarted)
                return -1;
            else
                return 0;
        }
        else
            return 0;
    })), [jobs]);
    const rows = useMemo(() => (sortedJobs.map((j) => ({
        key: j.jobId || 'null',
        columnValues: {
            jobId: {
                text: j.jobId,
                element: React.createElement(Hyperlink, { onClick: () => { onViewJob && onViewJob(j); } }, j.jobId)
            },
            functionName: {
                text: j.functionName
            },
            status: {
                text: j.status,
                element: j.status === 'running' ? (React.createElement("span", null,
                    React.createElement("span", null,
                        j.status,
                        " "),
                    React.createElement(CancelJobButton, { onClick: () => { onCancelJob && onCancelJob(j); } }))) : React.createElement("span", null, j.status)
            },
            started: { text: j.timestampStarted ? formatTime(new Date(j.timestampStarted)) : '' },
            finished: { text: j.timestampFinished ? formatTime(new Date(j.timestampFinished)) : '' },
            message: { text: j.error_message || '' }
        }
    }))), [sortedJobs]);
    return (React.createElement(NiceTable, { rows: rows, columns: columns }));
};
function niceStringify(x) {
    // TODO: figure out how to keep numeric arrays on one line in this expansion
    return JSON.stringify(x, null, 4);
}
function formatTime(d) {
    const datesAreOnSameDay = (first, second) => first.getFullYear() === second.getFullYear() &&
        first.getMonth() === second.getMonth() &&
        first.getDate() === second.getDate();
    let ret = '';
    if (!datesAreOnSameDay(d, new Date())) {
        ret += `${(d.getMonth() + 1)}/${d.getDate()}/${d.getFullYear()}} `;
    }
    ret += `${d.toLocaleTimeString()}`;
    return ret;
}
const CancelJobButton = ({ onClick }) => {
    return (React.createElement(IconButton, { title: "Cancel job", onClick: onClick },
        React.createElement(Delete, null)));
};
export default HitherJobMonitorTable;
//# sourceMappingURL=HitherJobMonitorTable.js.map