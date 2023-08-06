import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage } from 'app/actionCreators/indicator';
import ExternalLink from 'app/components/links/externalLink';
import List from 'app/components/list';
import ListItem from 'app/components/list/listItem';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import Form from 'app/views/settings/components/forms/form';
import NumberField from 'app/views/settings/components/forms/numberField';
import RadioField from 'app/views/settings/components/forms/radioField';
var impacts = [
    tct('[strong:Data glitches.] During reprocessing you may observe temporary data inconsistencies across the entire product. Those inconsistencies disappear the moment reprocessing is complete.', { strong: <strong /> }),
    tct('[strong:Attachment storage needs to be enabled.] If your events come from minidumps or unreal crash reports, you must have [link:attachment storage] enabled.', {
        strong: <strong />,
        link: (<ExternalLink href="https://docs.sentry.io/platforms/native/enriching-events/attachments/#crash-reports-and-privacy"/>),
    }),
    tct("[strong:Quota applies.] Every event you choose to reprocess will count against your plan's quota a second time. Rate limits and spike protection do not apply.", { strong: <strong /> }),
    t('Please wait one hour before attempting to reprocess missing debug files.'),
    t('Reprocessed events will not trigger issue alerts, and reprocessed events are not subject to data forwarding.'),
];
var remainingEventsChoices = [
    ['keep', t('Keep')],
    ['delete', t('Delete')],
];
var ReprocessingEventModal = /** @class */ (function (_super) {
    __extends(ReprocessingEventModal, _super);
    function ReprocessingEventModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { maxEvents: undefined };
        _this.handleSuccess = function () {
            var closeModal = _this.props.closeModal;
            closeModal();
            window.location.reload();
        };
        _this.handleMaxEventsChange = function (maxEvents) {
            _this.setState({ maxEvents: Number(maxEvents) || undefined });
        };
        return _this;
    }
    ReprocessingEventModal.prototype.handleError = function () {
        addErrorMessage(t('Failed to reprocess. Please check your input.'));
    };
    ReprocessingEventModal.prototype.render = function () {
        var _a = this.props, organization = _a.organization, Header = _a.Header, Body = _a.Body, closeModal = _a.closeModal, groupId = _a.groupId;
        var maxEvents = this.state.maxEvents;
        var orgSlug = organization.slug;
        var endpoint = "/organizations/" + orgSlug + "/issues/" + groupId + "/reprocessing/";
        var title = t('Reprocess Events');
        return (<React.Fragment>
        <Header closeButton>
          <span data-test-id="modal-title">{title}</span>
        </Header>
        <Body>
          <Introduction>
            {t('Reprocessing applies any new debug files or grouping configuration to an Issue. Before you give it a try, you should probably consider these impacts:')}
          </Introduction>
          <StyledList symbol="bullet">
            {impacts.map(function (impact, index) { return (<ListItem key={index}>{impact}</ListItem>); })}
          </StyledList>
          <Introduction>
            {tct('For more information please refer to [link:the documentation on reprocessing.]', {
                link: (<ExternalLink href="https://docs.sentry.io/product/error-monitoring/reprocessing/"/>),
            })}
          </Introduction>
          <Form submitLabel={title} apiEndpoint={endpoint} apiMethod="POST" initialData={{ maxEvents: undefined, remainingEvents: 'keep' }} onSubmitSuccess={this.handleSuccess} onSubmitError={this.handleError} onCancel={closeModal} footerClass="modal-footer">
            <NumberField name="maxEvents" label={t('Number of events to be reprocessed')} help={t('If you set a limit, we will reprocess your most recent events.')} placeholder={t('Reprocess all events')} onChange={this.handleMaxEventsChange} min={1}/>

            <RadioField orientInline label={t('Remaining events')} help={t('What to do with the events that are not reprocessed.')} name="remainingEvents" choices={remainingEventsChoices} disabled={maxEvents === undefined}/>
          </Form>
        </Body>
      </React.Fragment>);
    };
    return ReprocessingEventModal;
}(React.Component));
export default ReprocessingEventModal;
var Introduction = styled('p')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeLarge; });
var StyledList = styled(List)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  grid-gap: ", ";\n  margin-bottom: ", ";\n  font-size: ", ";\n"], ["\n  grid-gap: ", ";\n  margin-bottom: ", ";\n  font-size: ", ";\n"])), space(1), space(4), function (p) { return p.theme.fontSizeMedium; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=reprocessEventModal.jsx.map