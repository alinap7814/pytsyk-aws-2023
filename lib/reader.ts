import { load } from 'js-yaml'
import { readFileSync } from 'fs';


export class Reader {
    yaml(filePath: string): object {
        const content: string = readFileSync(filePath, "utf8")
        const contentObject: object = Object(load(content))
        return contentObject
    }
}