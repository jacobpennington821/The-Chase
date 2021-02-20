export abstract class ClientState {

    actions: Map<string, ClientStateAction>;

    constructor() {
        this.actions = new Map<string, ClientStateAction>();
    }

    public handleJSON(msg: any): ClientState | null {
        if (!("action" in msg)) {
            console.log("Malformed event: " + msg)
            return null;
        }
        return this.runAction(msg["action"], msg);
    }

    protected addAction(action: ClientStateAction) {
        this.actions.set(action.getName(), action);
    }

    public runAction(actionName: string, args: any): ClientState | null {
        let action: ClientStateAction | undefined = this.actions.get(actionName);
        if (action === undefined) {
            console.log("Tried to perform non-existent action " + actionName);
            return null;
        }
        return action.run(args);
    }

    public enterState(oldState: ClientState): ClientState | null {
        return null;
    }

    public exitState(): void {

    }
}

export class ClientStateAction {
    name: string;
    runCallback: (args: any) => ClientState | null;

    constructor(name: string, runCallback: (args: any) => ClientState | null) {
        this.name = name;
        this.runCallback = runCallback;
    }

    public run(args: any): ClientState | null {
        return this.runCallback(args);
    }

    public getName(): string {
        return this.name;
    }
}
