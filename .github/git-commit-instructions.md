# Commit Standards 📜

According to the **[Conventional Commits](https://www.conventionalcommits.org)** documentation, semantic commits are a simple convention to use in commit messages. This convention defines a set of rules to create an explicit commit history, which facilitates the creation of automated tools.

This identification occurs through a keyword and emoji that identifies whether the commit is a code change, package update, documentation, visual change, test...

## Type and Description 🦄

The semantic commit has the structural elements below (types), which inform the user of your code about the intention of your commit.

- `feat` - Commits of type `feat` indicate that your piece of code is including a **new feature** (relates to MINOR in semantic versioning).

- `fix` - Commits of type `fix` indicate that your committed code is **solving a problem** (bug fix), (relates to PATCH in semantic versioning).

- `docs` - Commits of type `docs` indicate that there have been **changes in the documentation**, such as in the Readme of your repository. (Does not include code changes).

- `test` - Commits of type `test` are used when **changes are made to tests**, whether creating, modifying, or deleting unit tests. (Does not include code changes)

- `build` - Commits of type `build` are used when modifications are made to **build files and dependencies**.

- `perf` - Commits of type `perf` serve to identify any code changes related to **performance**.

- `style` - Commits of type `style` indicate that there have been changes related to **code formatting**, semicolons, trailing spaces, lint... (Does not include code changes).

- `refactor` - Commits of type `refactor` refer to changes due to **refactoring that does not alter functionality**, for example, a change in the way a certain part of the screen is processed, but which maintained the same functionality, or performance improvements due to a code review.

- `chore` - Commits of type `chore` indicate **build task updates**, administrator configurations, packages... such as adding a package to gitignore. (Does not include code changes)

- `ci` - Commits of type `ci` indicate changes related to **continuous integration**.

- `raw` - Commits of type `raw` indicate changes related to configuration files, data, features, parameters.

- `cleanup` - Commits of type `cleanup` are used to remove commented code, unnecessary snippets, or any other form of source code cleanup, aiming to enhance its readability and maintainability.

- `remove` - Commits of type `remove` indicate the deletion of obsolete or unused files, directories, or functionalities, reducing the project's size and complexity and keeping it more organized.

## Recommendations 🎉

- Add a type consistent with the content's title.
- We recommend that the first line should have a maximum of 4 words.
- To describe in detail, use the commit description body.
- Use an emoji at the beginning of the commit message representing the commit.
- Links should be added in their most authentic form, i.e., without link shorteners and affiliate links.

## Commit Supplements 💻

- **Footer:** information about the reviewer and card number in Trello or Jira. Example: Reviewed-by: Vinicius Meireles Refs #133
- **Body:** more precise descriptions of what is contained in the commit, presenting impacts and the reasons why the code changes were made, as well as essential instructions for future interventions. Example: see the issue for details on typos fixed.
- **Descriptions:** a succinct description of the change. Example: correct minor typos in code

## Emoji Standards 💈

<table>
  <thead>
    <tr>
      <th>Commit Type</th>
      <th>Emoji</th>
      <th>Keyword</th>
    </tr>
  </thead>
 <tbody>
    <tr>
      <td>Accessibility</td>
      <td>♿ <code>:wheelchair:</code></td>
      <td></td>
    </tr>
    <tr>
      <td>Adding a test</td>
      <td>✅ <code>:white_check_mark:</code></td>
      <td><code>test</code></td>
    </tr>
    <tr>
      <td>Updating a submodule version</td>
      <td>⬆️ <code>:arrow_up:</code></td>
      <td></td>
    </tr>
    <tr>
      <td>Downgrading a submodule version</td>
      <td>⬇️ <code>:arrow_down:</code></td>
      <td></td>
    </tr>
    <tr>
      <td>Adding a dependency</td>
      <td>➕ <code>:heavy_plus_sign:</code></td>
      <td><code>build</code></td>
    </tr>
    <tr>
      <td>Code review changes</td>
      <td>👌 <code>:ok_hand:</code></td>
      <td><code>style</code></td>
    </tr>
    <tr>
      <td>Animations and transitions</td>
      <td>💫 <code>:dizzy:</code></td>
      <td></td>
    </tr>
    <tr>
      <td>Bugfix</td>
      <td>🐛 <code>:bug:</code></td>
      <td><code>fix</code></td>
    </tr>
    <tr>
      <td>Comments</td>
      <td>💡 <code>:bulb:</code></td>
      <td><code>docs</code></td>
    </tr>
    <tr>
      <td>Initial commit</td>
      <td>🎉 <code>:tada:</code></td>
      <td><code>init</code></td>
    </tr>
    <tr>
      <td>Configuration</td>
      <td>🔧 <code>:wrench:</code></td>
      <td><code>chore</code></td>
    </tr>
    <tr>
      <td>Deploy</td>
      <td>🚀 <code>:rocket:</code></td>
      <td></td>
    </tr>
    <tr>
      <td>Documentation</td>
      <td>📚 <code>:books:</code></td>
      <td><code>docs</code></td>
    </tr>
    <tr>
      <td>In progress</td>
      <td>🚧 <code>:construction:</code></td>
      <td></td>
    </tr>
    <tr>
      <td>UI Styling</td>
      <td>💄 <code>:lipstick:</code></td>
      <td><code>feat</code></td>
    </tr>
    <tr>
      <td>Infrastructure</td>
      <td>🧱 <code>:bricks:</code></td>
      <td><code>ci</code></td>
    </tr>
    <tr>
      <td>Idea list (tasks)</td>
      <td>🔜 <code> :soon: </code></td>
      <td></td>
    </tr>
    <tr>
      <td>Move/Rename</td>
      <td>🚚 <code>:truck:</code></td>
      <td><code>chore</code></td>
    </tr>
    <tr>
      <td>New feature</td>
      <td>✨ <code>:sparkles:</code></td>
      <td><code>feat</code></td>
    </tr>
    <tr>
      <td>Package.json in JS</td>
      <td>📦 <code>:package:</code></td>
      <td><code>build</code></td>
    </tr>
    <tr>
      <td>Performance</td>
      <td>⚡ <code>:zap:</code></td>
      <td><code>perf</code></td>
    </tr>
    <tr>
        <td>Refactoring</td>
        <td>♻️ <code>:recycle:</code></td>
        <td><code>refactor</code></td>
    </tr>
    <tr>
      <td>Code Cleanup</td>
      <td>🧹 <code>:broom:</code></td>
      <td><code>cleanup</code></td>
    </tr>
    <tr>
      <td>Removing a file</td>
      <td>🗑️ <code>:wastebasket:</code></td>
      <td><code>remove</code></td>
    </tr>
    <tr>
      <td>Removing a dependency</td>
      <td>➖ <code>:heavy_minus_sign:</code></td>
      <td><code>build</code></td>
    </tr>
    <tr>
      <td>Responsiveness</td>
      <td>📱 <code>:iphone:</code></td>
      <td></td>
    </tr>
    <tr>
      <td>Reverting changes</td>
      <td>💥 <code>:boom:</code></td>
      <td><code>fix</code></td>
    </tr>
    <tr>
      <td>Security</td>
      <td>🔒️ <code>:lock:</code></td>
      <td></td>
    </tr>
    <tr>
      <td>SEO</td>
      <td>🔍️ <code>:mag:</code></td>
      <td></td>
    </tr>
    <tr>
      <td>Version tag</td>
      <td>🔖 <code>:bookmark:</code></td>
      <td></td>
    </tr>
    <tr>
      <td>Approval test</td>
      <td>✔️ <code>:heavy_check_mark:</code></td>
      <td><code>test</code></td>
    </tr>
    <tr>
      <td>Tests</td>
      <td>🧪 <code>:test_tube:</code></td>
      <td><code>test</code></td>
    </tr>
    <tr>
      <td>Text</td>
      <td>📝 <code>:pencil:</code></td>
      <td></td>
    </tr>
    <tr>
      <td>Typing</td>
      <td>🏷️ <code>:label:</code></td>
      <td></td>
    </tr>
    <tr>
      <td>Error handling</td>
      <td>🥅 <code>:goal_net:</code></td>
      <td></td>
    </tr>
    <tr>
      <td>Data</td>
      <td>🗃️ <code>:card_file_box:</code></td>
      <td><code>raw</code></td>
    </tr>
  </tbody>
</table>

## 💻 Examples

<table>
  <thead>
    <tr>
      <th>Git Command</th>
      <th>Result on GitHub</th>
    </tr>
  </thead>
 <tbody>
    <tr>
      <td>
        <code>git commit -m ":tada: Initial commit"</code>
      </td>
      <td>🎉 Initial commit</td>
    </tr>
    <tr>
      <td>
        <code>git commit -m ":books: docs: README update"</code>
      </td>
      <td>📚 docs: README update</td>
    </tr>
    <tr>
      <td>
        <code>git commit -m ":bug: fix: Infinite loop on line 50"</code>
      </td>
      <td>🐛 fix: Infinite loop on line 50</td>
    </tr>
    <tr>
      <td>
        <code>git commit -m ":sparkles: feat: Login page"</code>
      </td>
      <td>✨ feat: Login page</td>
    </tr>
    <tr>
      <td>
        <code>git commit -m ":bricks: ci: Dockerfile modification"</code>
      </td>
      <td>🧱 ci: Dockerfile modification</td>
    </tr>
    <tr>
      <td>
        <code>git commit -m ":recycle: refactor: Converting to arrow functions"</code>
      </td>
      <td>♻️ refactor: Converting to arrow functions</td>
    </tr>
    <tr>
      <td>
        <code>git commit -m ":zap: perf: Improved response time"</code>
      </td>
      <td>⚡ perf: Improved response time</td>
    </tr>
    <tr>
      <td>
        <code>git commit -m ":boom: fix: Reverting inefficient changes"</code>
      </td>
      <td>💥 fix: Reverting inefficient changes</td>
    </tr>
    <tr>
      <td>
        <code>git commit -m ":lipstick: feat: CSS styling for the form"</code>
      </td>
      <td>💄 feat: CSS styling for the form</td>
    </tr>
    <tr>
      <td>
        <code>git commit -m ":test_tube: test: Creating new test"</code>
      </td>
      <td>🧪 test: Creating new test</td>
    </tr>
    <tr>
      <td>
        <code>git commit -m ":bulb: docs: Comments on the LoremIpsum( ) function"</code>
      </td>
      <td>💡 docs: Comments on the LoremIpsum( ) function</td>
    </tr>
    <tr>
      <td>
        <code>git commit -m ":card_file_box: raw: RAW Data for year yyyy"</code>
      </td>
      <td>🗃️ raw: RAW Data for year yyyy</td>
    </tr>
    <tr>
      <td>
        <code>git commit -m ":broom: cleanup: Removing commented code blocks and unused variables in the form validation function"</code>
      </td>
      <td>🧹 cleanup: Removing commented code blocks and unused variables in the form validation function</td>
    </tr>
    <tr>
      <td>
        <code>git commit -m ":wastebasket: remove: Removing unused project files to maintain organization and continuous updating"</code>
      </td>
      <td>🗑️ remove: Removing unused project files to maintain organization and continuous updating</td>
    </tr>
  </tbody>
</table>