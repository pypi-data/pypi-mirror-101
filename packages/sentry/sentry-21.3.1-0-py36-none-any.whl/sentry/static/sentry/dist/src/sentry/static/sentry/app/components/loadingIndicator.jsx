import React from 'react';
import { withProfiler } from '@sentry/react';
import classNames from 'classnames';
import sentryLoader from 'sentry-images/sentry-loader.svg';
function renderLogoSpinner() {
    return <img src={sentryLoader}/>;
}
function LoadingIndicator(props) {
    var hideMessage = props.hideMessage, mini = props.mini, triangle = props.triangle, overlay = props.overlay, dark = props.dark, children = props.children, finished = props.finished, className = props.className, style = props.style, relative = props.relative, size = props.size, hideSpinner = props.hideSpinner;
    var cx = classNames(className, {
        overlay: overlay,
        dark: dark,
        loading: true,
        mini: mini,
        triangle: triangle,
    });
    var loadingCx = classNames({
        relative: relative,
        'loading-indicator': true,
        'load-complete': finished,
    });
    var loadingStyle = {};
    if (size) {
        loadingStyle = {
            width: size,
            height: size,
        };
    }
    return (<div className={cx} style={style}>
      {!hideSpinner && (<div className={loadingCx} style={loadingStyle}>
          {triangle && renderLogoSpinner()}
          {finished ? <div className="checkmark draw" style={style}/> : null}
        </div>)}
      {!hideMessage && <div className="loading-message">{children}</div>}
    </div>);
}
export default withProfiler(LoadingIndicator, {
    includeUpdates: false,
});
//# sourceMappingURL=loadingIndicator.jsx.map