import React from 'react';
import { useState } from "react";
import Hyperlink from "../../common/Hyperlink";
import { Button, Table, TableBody, TableCell, TableHead, TableRow } from "@material-ui/core";
const HitherJobMonitorJobView = ({ job, onBack }) => {
    return (React.createElement("div", null,
        React.createElement("p", null,
            React.createElement(Hyperlink, { onClick: onBack }, "Back to jobs")),
        React.createElement(HitherJobInfoView, { job: job })));
};
const HitherJobInfoView = ({ job }) => {
    const argumentsCollapsable = (job.kwargs && niceStringify(job.kwargs).length > 50);
    const logArgumentsToConsole = (job.kwargs && niceStringify(job.kwargs).length > 1000);
    const [argumentsExpanded, setArgumentsExpanded] = useState(!argumentsCollapsable);
    const resultCollapsable = (job.result && niceStringify(job.result).length > 50);
    const logResultToConsole = (job.result && niceStringify(job.result).length > 1000);
    const [resultExpanded, setResultExpanded] = useState(!resultCollapsable);
    const argumentsElement = argumentsExpanded ? (React.createElement("div", null,
        argumentsCollapsable && React.createElement(Button, { onClick: () => setArgumentsExpanded(false) }, "Collapse"),
        React.createElement("pre", null, job.kwargs ? niceStringify(job.kwargs) : ''))) : (logArgumentsToConsole ? (React.createElement(Button, { onClick: () => { console.info(job.kwargs); }, title: "Write input argumetns to the browser developer tools console" }, "Write input arguments to console")) : (React.createElement(Button, { onClick: () => { console.info(job.kwargs); setArgumentsExpanded(true); } }, "Expand")));
    const resultElement = resultExpanded ? (React.createElement("div", null,
        resultCollapsable && React.createElement(Button, { onClick: () => setResultExpanded(false) }, "Collapse"),
        React.createElement("pre", null, job.result ? niceStringify(job.result) : ''))) : (logResultToConsole ? (React.createElement(Button, { onClick: () => { console.info(job.result); }, title: "Write result to the browser developer tools console" }, "Write result to console")) : (React.createElement(Button, { onClick: () => { console.info(job.result); setResultExpanded(true); } }, "Expand")));
    const fields = [
        {
            label: 'Job ID',
            value: job.jobId
        },
        {
            label: 'Function name',
            value: job.functionName
        },
        {
            label: 'Input arguments',
            value: argumentsElement
        },
        {
            label: 'Status',
            value: job.status
        },
        {
            label: 'Started',
            value: job.timestampStarted ? formatTime(new Date(job.timestampStarted)) : ''
        },
        {
            label: 'Finished',
            value: job.timestampFinished ? formatTime(new Date(job.timestampFinished)) : ''
        },
        {
            label: 'Result',
            value: resultElement
        },
        {
            label: 'Error message',
            value: job.error_message
        }
    ];
    return (React.createElement("div", null,
        React.createElement(Table, { className: "NiceTable" },
            React.createElement(TableHead, null),
            React.createElement(TableBody, null, fields.map(f => (React.createElement(TableRow, { key: f.label },
                React.createElement(TableCell, null, f.label),
                React.createElement(TableCell, null, f.value))))))));
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
export default HitherJobMonitorJobView;
//# sourceMappingURL=HitherJobMonitorJobView.js.map