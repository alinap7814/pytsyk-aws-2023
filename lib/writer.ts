import { Reader } from '../lib/reader'
import { getEnvironment } from './environment'



export class Writer {
    getEnvironmentAccounts(): object {
        const reader = new Reader()
        const environment: string = getEnvironment()
        const localAccounts: any = reader.yaml('accounts.yml')
        const environmentAccounts: object = (localAccounts[environment] === undefined) ? localAccounts['dev'] : localAccounts[environment];
        return environmentAccounts
    }
}
