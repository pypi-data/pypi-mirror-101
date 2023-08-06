import { HitherJob } from 'labbox';
import { FunctionComponent } from "react";
declare const HitherJobMonitorTable: FunctionComponent<{
    jobs: HitherJob[];
    onViewJob: (job: HitherJob) => void;
    onCancelJob: (job: HitherJob) => void;
}>;
export default HitherJobMonitorTable;
