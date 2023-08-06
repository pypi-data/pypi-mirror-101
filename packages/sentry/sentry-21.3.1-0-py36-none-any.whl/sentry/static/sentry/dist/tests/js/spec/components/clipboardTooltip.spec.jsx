import React from 'react';
import { mountWithTheme } from 'sentry-test/enzyme';
import ClipboardTooltip from 'app/components/clipboardTooltip';
import { OPEN_DELAY } from 'app/components/tooltip';
describe('ClipboardTooltip', function () {
    it('renders', function () {
        var title = 'tooltip content';
        var wrapper = mountWithTheme(<ClipboardTooltip title={title}>
        <span>This text displays a tooltip when hovering</span>
      </ClipboardTooltip>);
        jest.useFakeTimers();
        var trigger = wrapper.find('span');
        trigger.simulate('mouseEnter');
        jest.advanceTimersByTime(OPEN_DELAY);
        wrapper.update();
        var tooltipClipboardWrapper = wrapper.find('TooltipClipboardWrapper');
        expect(tooltipClipboardWrapper.length).toEqual(1);
        var tooltipTextContent = tooltipClipboardWrapper.find('TextOverflow');
        expect(tooltipTextContent.length).toEqual(1);
        var clipboardContent = tooltipClipboardWrapper.find('Clipboard');
        expect(clipboardContent.length).toEqual(1);
        expect(clipboardContent.props().value).toEqual(title);
        var iconCopy = clipboardContent.find('IconCopy');
        expect(iconCopy.length).toEqual(1);
    });
});
//# sourceMappingURL=clipboardTooltip.spec.jsx.map