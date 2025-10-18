module.exports = {
  testEnvironment: 'node',
  testMatch: ['**/*.test.js', '**/*.test.ts'],
  transform: {
    '^.+\\.ts$': ['ts-jest', { useESM: true }],
  },
  moduleFileExtensions: ['js', 'ts'],
  collectCoverageFrom: ['*.js', '*.ts', '!*.test.js', '!*.test.ts'],
};
