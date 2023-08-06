import { HitherJob } from 'labbox';
import { FunctionComponent } from 'react';
declare type Props = {
    onClick?: () => void;
};
export declare const useMonitorHitherJobs: () => {
    pendingJobs: HitherJob[];
    runningJobs: HitherJob[];
    finishedJobs: HitherJob[];
    erroredJobs: HitherJob[];
    allJobs: HitherJob[];
};
declare const HitherJobMonitorControl: FunctionComponent<Props>;
export default HitherJobMonitorControl;
