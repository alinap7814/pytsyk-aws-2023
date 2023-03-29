import { execSync } from 'child_process'

const gitCommand = 'git rev-parse --abbrev-ref HEAD'

function getBranch() {
    return execSync(gitCommand).toString().trim()
}


export function getEnvironment() {
    const branchName = getBranch()
    return branchName === 'master' ? 'prod' : branchName
}
