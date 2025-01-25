const { override } = require("customize-cra");

module.exports = override((config) => {
  config.module.rules = config.module.rules.filter(
    (rule) => !/source-map-loader/.test(rule.loader || "")
  );
  return config;
});
