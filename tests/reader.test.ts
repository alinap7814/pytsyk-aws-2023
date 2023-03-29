import { Reader } from "../lib/reader";
import * as fs from 'fs'


describe("test reader", () => {
    const reader = new Reader();
    const testAccountFileContent = `dev:\n Name: testAccount`
    jest.spyOn(fs, 'readFileSync').mockReturnValueOnce(testAccountFileContent);
    const content: any = reader.yaml('testPath')
    test("get environment", () => {
        expect(content).toMatchObject({ dev: { Name: 'testAccount' } });
    });

});