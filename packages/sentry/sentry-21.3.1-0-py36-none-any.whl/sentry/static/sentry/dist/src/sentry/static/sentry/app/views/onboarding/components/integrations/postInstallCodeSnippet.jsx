import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
export default function PostInstallCodeSnippet(_a) {
    var provider = _a.provider, platform = _a.platform, isOnboarding = _a.isOnboarding;
    //currently supporting both Python and Node
    var token_punctuation = platform === 'python-awslambda' ? '()' : '();';
    return (<div>
      <p>
        {t("Congrats, you just installed the %s integration! Now that it's is installed, the next time you trigger an error it will go to your Sentry.", provider.name)}
      </p>
      <p>
        {t('This snippet includes an intentional error, so you can test that everything is working as soon as you set it up:')}
      </p>
      <div>
        <CodeWrapper>
          <code>
            <TokenFunction>myUndefinedFunction</TokenFunction>
            <TokenPunctuation>{token_punctuation}</TokenPunctuation>)
          </code>
        </CodeWrapper>
      </div>
      {isOnboarding && (<React.Fragment>
          <p>
            {t("If you're new to Sentry, use the email alert to access your account and complete a product tour.")}
          </p>
          <p>
            {t("If you're an existing user and have disabled alerts, you won't receive this email.")}
          </p>
        </React.Fragment>)}
    </div>);
}
var CodeWrapper = styled('pre')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 1em;\n  overflow: auto;\n  background: #251f3d;\n  font-size: 15px;\n"], ["\n  padding: 1em;\n  overflow: auto;\n  background: #251f3d;\n  font-size: 15px;\n"])));
var TokenFunction = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: #7cc5c4;\n"], ["\n  color: #7cc5c4;\n"])));
var TokenPunctuation = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: #b3acc1;\n"], ["\n  color: #b3acc1;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=postInstallCodeSnippet.jsx.map