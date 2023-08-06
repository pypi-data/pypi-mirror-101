import { __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import DateTime from 'app/components/dateTime';
import { getTraceDateTimeRange } from 'app/components/events/interfaces/spans/utils';
import Link from 'app/components/links/link';
import { ALL_ACCESS_PROJECTS } from 'app/constants/globalSelectionHeader';
import { IconWarning } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import EventView from 'app/utils/discover/eventView';
import { eventDetailsRoute, generateEventSlug } from 'app/utils/discover/urls';
import getDynamicText from 'app/utils/getDynamicText';
import { WEB_VITAL_DETAILS } from 'app/utils/performance/vitals/constants';
import { QueryResults, stringifyQueryObject } from 'app/utils/tokenizeSearch';
import { transactionSummaryRouteWithQuery } from 'app/views/performance/transactionSummary/utils';
import { getTransactionDetailsUrl } from 'app/views/performance/utils';
import { Row, Tags, TransactionDetails, TransactionDetailsContainer } from './styles';
var TransactionDetail = /** @class */ (function (_super) {
    __extends(TransactionDetail, _super);
    function TransactionDetail() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TransactionDetail.prototype.renderSingleErrorMessage = function (error) {
        var organization = this.props.organization;
        var eventSlug = generateEventSlug({
            id: error.event_id,
            project: error.project_slug,
        });
        var target = {
            pathname: eventDetailsRoute({
                orgSlug: organization.slug,
                eventSlug: eventSlug,
            }),
        };
        return (<Link to={target}>
        <span>{t('An error event occurred in this transaction.')}</span>
      </Link>);
    };
    TransactionDetail.prototype.renderMultiErrorMessage = function (errors) {
        var _a = this.props, organization = _a.organization, transaction = _a.transaction;
        var _b = getTraceDateTimeRange({
            start: transaction.start_timestamp,
            end: transaction.timestamp,
        }), start = _b.start, end = _b.end;
        var queryResults = new QueryResults([]);
        var eventIds = errors.map(function (child) { return child.event_id; });
        for (var i = 0; i < eventIds.length; i++) {
            queryResults.addOp(i === 0 ? '(' : 'OR');
            queryResults.addQuery("id:" + eventIds[i]);
            if (i === eventIds.length - 1) {
                queryResults.addOp(')');
            }
        }
        var eventView = EventView.fromSavedQuery({
            id: undefined,
            name: "Errors events associated with transaction " + transaction.event_id,
            fields: ['title', 'project', 'issue', 'timestamp'],
            orderby: '-timestamp',
            query: stringifyQueryObject(queryResults),
            projects: organization.features.includes('global-views')
                ? [ALL_ACCESS_PROJECTS]
                : __spreadArray([], __read(new Set(errors.map(function (error) { return error.project_id; })))),
            version: 2,
            start: start,
            end: end,
        });
        var target = eventView.getResultsViewUrlTarget(organization.slug);
        return (<div>
        {tct('[link] occured in this transaction.', {
                link: (<Link to={target}>
              <span>{t('%d error events', errors.length)}</span>
            </Link>),
            })}
      </div>);
    };
    TransactionDetail.prototype.renderTransactionErrors = function () {
        var transaction = this.props.transaction;
        var errors = transaction.errors;
        if (errors.length === 0) {
            return null;
        }
        var message = errors.length === 1
            ? this.renderSingleErrorMessage(errors[0])
            : this.renderMultiErrorMessage(errors);
        return (<Alert system type="error" icon={<IconWarning size="md"/>}>
        {message}
      </Alert>);
    };
    TransactionDetail.prototype.renderGoToTransactionButton = function () {
        var _a = this.props, location = _a.location, organization = _a.organization, transaction = _a.transaction;
        var eventSlug = generateEventSlug({
            id: transaction.event_id,
            project: transaction.project_slug,
        });
        var target = getTransactionDetailsUrl(organization, eventSlug, transaction.transaction, location.query);
        return (<StyledButton size="xsmall" to={target}>
        {t('View Transaction')}
      </StyledButton>);
    };
    TransactionDetail.prototype.renderGoToSummaryButton = function () {
        var _a = this.props, location = _a.location, organization = _a.organization, transaction = _a.transaction;
        var target = transactionSummaryRouteWithQuery({
            orgSlug: organization.slug,
            transaction: transaction.transaction,
            query: location.query,
            projectID: String(transaction.project_id),
        });
        return (<StyledButton size="xsmall" to={target}>
        {t('View Summary')}
      </StyledButton>);
    };
    TransactionDetail.prototype.renderMeasurements = function () {
        var transaction = this.props.transaction;
        var _a = transaction.measurements, measurements = _a === void 0 ? {} : _a;
        var measurementKeys = Object.keys(measurements)
            .filter(function (name) { return Boolean(WEB_VITAL_DETAILS["measurements." + name]); })
            .sort();
        if (measurementKeys.length <= 0) {
            return null;
        }
        return (<React.Fragment>
        {measurementKeys.map(function (measurement) {
                var _a;
                return (<Row key={measurement} title={(_a = WEB_VITAL_DETAILS["measurements." + measurement]) === null || _a === void 0 ? void 0 : _a.name}>
            {Number(measurements[measurement].value.toFixed(3)).toLocaleString() + "ms"}
          </Row>);
            })}
      </React.Fragment>);
    };
    TransactionDetail.prototype.renderTransactionDetail = function () {
        var _a = this.props, location = _a.location, organization = _a.organization, transaction = _a.transaction;
        var startTimestamp = Math.min(transaction.start_timestamp, transaction.timestamp);
        var endTimestamp = Math.max(transaction.start_timestamp, transaction.timestamp);
        var duration = (endTimestamp - startTimestamp) * 1000;
        var durationString = Number(duration.toFixed(3)).toLocaleString() + "ms";
        return (<TransactionDetails>
        <table className="table key-value">
          <tbody>
            <Row title="Transaction ID" extra={this.renderGoToTransactionButton()}>
              {transaction.event_id}
            </Row>
            <Row title="Transaction" extra={this.renderGoToSummaryButton()}>
              {transaction.transaction}
            </Row>
            <Row title="Transaction Status">{transaction['transaction.status']}</Row>
            <Row title="Start Date">
              {getDynamicText({
                fixed: 'Mar 19, 2021 11:06:27 AM UTC',
                value: (<React.Fragment>
                    <DateTime date={startTimestamp * 1000}/>
                    {" (" + startTimestamp + ")"}
                  </React.Fragment>),
            })}
            </Row>
            <Row title="End Date">
              {getDynamicText({
                fixed: 'Mar 19, 2021 11:06:28 AM UTC',
                value: (<React.Fragment>
                    <DateTime date={endTimestamp * 1000}/>
                    {" (" + endTimestamp + ")"}
                  </React.Fragment>),
            })}
            </Row>
            <Row title="Duration">{durationString}</Row>
            <Row title="Operation">{transaction['transaction.op'] || ''}</Row>
            {this.renderMeasurements()}
            <Tags location={location} organization={organization} transaction={transaction}/>
          </tbody>
        </table>
      </TransactionDetails>);
    };
    TransactionDetail.prototype.render = function () {
        return (<TransactionDetailsContainer onClick={function (event) {
                // prevent toggling the transaction detail
                event.stopPropagation();
            }}>
        {this.renderTransactionErrors()}
        {this.renderTransactionDetail()}
      </TransactionDetailsContainer>);
    };
    return TransactionDetail;
}(React.Component));
var StyledButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n"], ["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n"])), space(0.75), space(0.5));
export default TransactionDetail;
var templateObject_1;
//# sourceMappingURL=transactionDetail.jsx.map