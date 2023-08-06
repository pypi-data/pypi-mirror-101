module.exports = {
  branches: [
    { name: "stable" },
    { name: "next", prerelease: "rc", channel: false },
  ],
  // Define plugins used
  plugins: [
    // # Use default options for commit-analyzer
    "@semantic-release/commit-analyzer",
    // We need to tell semantic release how it can generate URL for commits and issues
    // See: https://github.com/semantic-release/release-notes-generator/issues/119#issuecomment-614189962
    [
      "@semantic-release/release-notes-generator",
      {
        preset: "conventionalcommits",
        writerOpts: {
          commitsSort: ["subject", "scope"],
        },
      },
    ],
    // Write changelog into CHANGELOG.md
    ["@semantic-release/changelog", { changelogFile: "CHANGELOG.md" }],
    // # Use custom script to perform release
    [
      "@semantic-release/exec",
      {
        prepareCmd:
          "python -m kapla.cli release prepare --version ${nextRelease.version} --branch ${branch.name}",
        publishCmd:
          "python -m kapla.cli release publish --branch ${branch.name}",
        successCmd:
          "python -m kapla.cli release success --branch ${branch.name}",
      },
    ],
  ],
};
