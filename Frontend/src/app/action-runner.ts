export interface ActionRunner {
    runAction(actionName: string, args: any): void;
}
