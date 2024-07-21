if (typeof process === 'undefined') {
    (window as any).process = {
        env: {}
    }
}