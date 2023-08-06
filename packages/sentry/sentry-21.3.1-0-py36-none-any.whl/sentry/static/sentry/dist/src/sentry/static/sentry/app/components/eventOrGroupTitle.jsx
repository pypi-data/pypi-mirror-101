import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import { getTitle } from 'app/utils/events';
import withOrganization from 'app/utils/withOrganization';
import StacktracePreview from './stacktracePreview';
var EventOrGroupTitle = /** @class */ (function (_super) {
    __extends(EventOrGroupTitle, _super);
    function EventOrGroupTitle() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EventOrGroupTitle.prototype.render = function () {
        var _a = this.props, hasGuideAnchor = _a.hasGuideAnchor, data = _a.data, organization = _a.organization, withStackTracePreview = _a.withStackTracePreview, guideAnchorName = _a.guideAnchorName;
        var _b = getTitle(data, organization), title = _b.title, subtitle = _b.subtitle;
        var titleWithHoverStacktrace = (<StacktracePreview organization={organization} issueId={data.id} disablePreview={!withStackTracePreview}>
        {title}
      </StacktracePreview>);
        return subtitle ? (<span style={this.props.style}>
        <GuideAnchor disabled={!hasGuideAnchor} target={guideAnchorName} position="bottom">
          <span>{titleWithHoverStacktrace}</span>
        </GuideAnchor>
        <Spacer />
        <Subtitle title={subtitle}>{subtitle}</Subtitle>
        <br />
      </span>) : (<span style={this.props.style}>
        <GuideAnchor disabled={!hasGuideAnchor} target={guideAnchorName} position="bottom">
          {titleWithHoverStacktrace}
        </GuideAnchor>
      </span>);
    };
    EventOrGroupTitle.defaultProps = {
        guideAnchorName: 'issue_title',
    };
    return EventOrGroupTitle;
}(React.Component));
export default withOrganization(EventOrGroupTitle);
/**
 * &nbsp; is used instead of margin/padding to split title and subtitle
 * into 2 separate text nodes on the HTML AST. This allows the
 * title to be highlighted without spilling over to the subtitle.
 */
var Spacer = function () { return <span style={{ display: 'inline-block', width: 10 }}>&nbsp;</span>; };
var Subtitle = styled('em')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  font-style: normal;\n"], ["\n  color: ", ";\n  font-style: normal;\n"])), function (p) { return p.theme.gray300; });
var templateObject_1;
//# sourceMappingURL=eventOrGroupTitle.jsx.map