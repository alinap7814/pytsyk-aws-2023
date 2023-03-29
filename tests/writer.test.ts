import { Writer } from "../lib/writer";
import * as fs from 'fs'




describe("get local accounts test reader", () => {
    jest.mock('../lib/environment', () => {
        return jest.fn().mockImplementation(() => { return 'dev' })
    });
    jest.mock('../lib/reader', () => {
        yaml: () => { dev: { test: 'account' } }
    });
    const writer = new Writer();
    const content: any = writer.getEnvironmentAccounts()
    test("local accounts", () => {

        console.log(content)
        // expect(roleSessionName).toBe("leonardo.bautista@accenture.com");
    });
});