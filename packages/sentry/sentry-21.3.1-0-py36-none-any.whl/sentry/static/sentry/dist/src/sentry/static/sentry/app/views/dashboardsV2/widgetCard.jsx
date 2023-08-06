import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import * as ReactRouter from 'react-router';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import classNames from 'classnames';
import isEqual from 'lodash/isEqual';
import { HeaderTitle } from 'app/components/charts/styles';
import DropdownMenu from 'app/components/dropdownMenu';
import ErrorBoundary from 'app/components/errorBoundary';
import MenuItem from 'app/components/menuItem';
import { isSelectionEqual } from 'app/components/organizations/globalSelectionHeader/utils';
import { Panel } from 'app/components/panels';
import Placeholder from 'app/components/placeholder';
import { IconDelete, IconEdit, IconEllipsis, IconGrabbable } from 'app/icons';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import { eventViewFromWidget } from './utils';
import WidgetCardChart from './widgetCardChart';
import WidgetQueries from './widgetQueries';
var WidgetCard = /** @class */ (function (_super) {
    __extends(WidgetCard, _super);
    function WidgetCard() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    WidgetCard.prototype.shouldComponentUpdate = function (nextProps) {
        if (!isEqual(nextProps.widget, this.props.widget) ||
            !isSelectionEqual(nextProps.selection, this.props.selection) ||
            this.props.isEditing !== nextProps.isEditing ||
            this.props.isSorting !== nextProps.isSorting ||
            this.props.hideToolbar !== nextProps.hideToolbar) {
            return true;
        }
        return false;
    };
    WidgetCard.prototype.renderToolbar = function () {
        var _a = this.props, onEdit = _a.onEdit, onDelete = _a.onDelete, draggableProps = _a.draggableProps, hideToolbar = _a.hideToolbar, isEditing = _a.isEditing;
        if (!isEditing) {
            return null;
        }
        return (<ToolbarPanel>
        <IconContainer style={{ visibility: hideToolbar ? 'hidden' : 'visible' }}>
          <IconClick>
            <StyledIconGrabbable color="textColor" {...draggableProps === null || draggableProps === void 0 ? void 0 : draggableProps.listeners} {...draggableProps === null || draggableProps === void 0 ? void 0 : draggableProps.attributes}/>
          </IconClick>
          <IconClick data-test-id="widget-edit" onClick={function () {
                onEdit();
            }}>
            <IconEdit color="textColor"/>
          </IconClick>
          <IconClick data-test-id="widget-delete" onClick={function () {
                onDelete();
            }}>
            <IconDelete color="textColor"/>
          </IconClick>
        </IconContainer>
      </ToolbarPanel>);
    };
    WidgetCard.prototype.renderContextMenu = function () {
        var _this = this;
        var _a = this.props, widget = _a.widget, selection = _a.selection, organization = _a.organization, showContextMenu = _a.showContextMenu;
        if (!showContextMenu) {
            return null;
        }
        var menuOptions = [];
        if (widget.displayType === 'table' &&
            organization.features.includes('discover-basic')) {
            // Open table widget in Discover
            if (widget.queries.length) {
                // We expect Table widgets to have only one query.
                var query = widget.queries[0];
                var eventView_1 = eventViewFromWidget(widget.title, query, selection);
                menuOptions.push(<MenuItem key="open-discover" onClick={function (event) {
                        event.preventDefault();
                        trackAnalyticsEvent({
                            eventKey: 'dashboards2.tablewidget.open_in_discover',
                            eventName: 'Dashboards2: Table Widget - Open in Discover',
                            organization_id: parseInt(_this.props.organization.id, 10),
                        });
                        browserHistory.push(eventView_1.getResultsViewUrlTarget(organization.slug));
                    }}>
            {t('Open in Discover')}
          </MenuItem>);
            }
        }
        if (!menuOptions.length) {
            return null;
        }
        return (<ContextWrapper>
        <ContextMenu>{menuOptions}</ContextMenu>
      </ContextWrapper>);
    };
    WidgetCard.prototype.render = function () {
        var _this = this;
        var _a = this.props, widget = _a.widget, api = _a.api, organization = _a.organization, selection = _a.selection, renderErrorMessage = _a.renderErrorMessage, location = _a.location, router = _a.router;
        return (<ErrorBoundary customComponent={<ErrorCard>{t('Error loading widget data')}</ErrorCard>}>
        <StyledPanel isDragging={false}>
          <WidgetHeader>
            <WidgetTitle>{widget.title}</WidgetTitle>
            {this.renderContextMenu()}
          </WidgetHeader>
          <WidgetQueries api={api} organization={organization} widget={widget} selection={selection}>
            {function (_a) {
                var tableResults = _a.tableResults, timeseriesResults = _a.timeseriesResults, errorMessage = _a.errorMessage, loading = _a.loading;
                return (<React.Fragment>
                  {typeof renderErrorMessage === 'function'
                        ? renderErrorMessage(errorMessage)
                        : null}
                  <WidgetCardChart timeseriesResults={timeseriesResults} tableResults={tableResults} errorMessage={errorMessage} loading={loading} location={location} widget={widget} selection={selection} router={router} organization={organization}/>
                  {_this.renderToolbar()}
                </React.Fragment>);
            }}
          </WidgetQueries>
        </StyledPanel>
      </ErrorBoundary>);
    };
    return WidgetCard;
}(React.Component));
export default withApi(withOrganization(withGlobalSelection(ReactRouter.withRouter(WidgetCard))));
var ErrorCard = styled(Placeholder)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  background-color: ", ";\n  border: 1px solid ", ";\n  color: ", ";\n  border-radius: ", ";\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  background-color: ", ";\n  border: 1px solid ", ";\n  color: ", ";\n  border-radius: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.alert.error.backgroundLight; }, function (p) { return p.theme.alert.error.border; }, function (p) { return p.theme.alert.error.textLight; }, function (p) { return p.theme.borderRadius; }, space(2));
var StyledPanel = styled(Panel, {
    shouldForwardProp: function (prop) { return prop !== 'isDragging'; },
})(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: 0;\n  visibility: ", ";\n  /* If a panel overflows due to a long title stretch its grid sibling */\n  height: 100%;\n  min-height: 96px;\n"], ["\n  margin: 0;\n  visibility: ", ";\n  /* If a panel overflows due to a long title stretch its grid sibling */\n  height: 100%;\n  min-height: 96px;\n"])), function (p) { return (p.isDragging ? 'hidden' : 'visible'); });
var ToolbarPanel = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  left: 0;\n  z-index: 1;\n\n  width: 100%;\n  height: 100%;\n\n  display: flex;\n  justify-content: flex-end;\n  align-items: flex-start;\n\n  background-color: ", ";\n  border-radius: ", ";\n"], ["\n  position: absolute;\n  top: 0;\n  left: 0;\n  z-index: 1;\n\n  width: 100%;\n  height: 100%;\n\n  display: flex;\n  justify-content: flex-end;\n  align-items: flex-start;\n\n  background-color: ", ";\n  border-radius: ", ";\n"])), function (p) { return p.theme.overlayBackgroundAlpha; }, function (p) { return p.theme.borderRadius; });
var IconContainer = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  margin: 10px ", ";\n  touch-action: none;\n"], ["\n  display: flex;\n  margin: 10px ", ";\n  touch-action: none;\n"])), space(2));
var IconClick = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  padding: ", ";\n\n  &:hover {\n    cursor: pointer;\n  }\n"], ["\n  padding: ", ";\n\n  &:hover {\n    cursor: pointer;\n  }\n"])), space(1));
var StyledIconGrabbable = styled(IconGrabbable)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  &:hover {\n    cursor: grab;\n  }\n"], ["\n  &:hover {\n    cursor: grab;\n  }\n"])));
var WidgetTitle = styled(HeaderTitle)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis);
var WidgetHeader = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  padding: ", " ", " 0 ", ";\n  width: 100%;\n  display: flex;\n  justify-content: space-between;\n"], ["\n  padding: ", " ", " 0 ", ";\n  width: 100%;\n  display: flex;\n  justify-content: space-between;\n"])), space(2), space(3), space(3));
var ContextMenu = function (_a) {
    var children = _a.children;
    return (<DropdownMenu>
    {function (_a) {
            var isOpen = _a.isOpen, getRootProps = _a.getRootProps, getActorProps = _a.getActorProps, getMenuProps = _a.getMenuProps;
            var topLevelCx = classNames('dropdown', {
                'anchor-right': true,
                open: isOpen,
            });
            return (<MoreOptions {...getRootProps({
                className: topLevelCx,
            })}>
          <DropdownTarget {...getActorProps({
                onClick: function (event) {
                    event.stopPropagation();
                    event.preventDefault();
                },
            })}>
            <IconEllipsis data-test-id="context-menu" size="md"/>
          </DropdownTarget>
          {isOpen && (<ul {...getMenuProps({})} className={classNames('dropdown-menu')}>
              {children}
            </ul>)}
        </MoreOptions>);
        }}
  </DropdownMenu>);
};
var MoreOptions = styled('span')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  display: flex;\n  color: ", ";\n"], ["\n  display: flex;\n  color: ", ";\n"])), function (p) { return p.theme.textColor; });
var DropdownTarget = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  display: flex;\n  cursor: pointer;\n"], ["\n  display: flex;\n  cursor: pointer;\n"])));
var ContextWrapper = styled('div')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11;
//# sourceMappingURL=widgetCard.jsx.map