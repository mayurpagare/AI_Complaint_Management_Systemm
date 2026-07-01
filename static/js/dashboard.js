document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-chart-source]").forEach((container) => {
        const data = JSON.parse(container.dataset.chartSource || "{}");
        container.querySelectorAll("canvas[data-chart]").forEach((canvas) => {
            const type = canvas.dataset.chart;
            if (type === "monthly") {
                drawBarChart(canvas, data.monthly || {});
            } else {
                drawPieChart(canvas, data[type] || {});
            }
        });
    });
});

const palette = ["#2563eb", "#14b8a6", "#f59e0b", "#ef4444", "#8b5cf6", "#22c55e", "#0ea5e9", "#f97316"];

function prepareCanvas(canvas) {
    const rect = canvas.getBoundingClientRect();
    const ratio = window.devicePixelRatio || 1;
    canvas.width = Math.max(320, rect.width) * ratio;
    canvas.height = Math.max(240, rect.height || 250) * ratio;
    const ctx = canvas.getContext("2d");
    ctx.scale(ratio, ratio);
    return { ctx, width: canvas.width / ratio, height: canvas.height / ratio };
}

function drawPieChart(canvas, rawData) {
    const { ctx, width, height } = prepareCanvas(canvas);
    const entries = Object.entries(rawData).filter(([, value]) => Number(value) > 0);
    ctx.clearRect(0, 0, width, height);
    if (!entries.length) {
        drawEmpty(ctx, width, height);
        return;
    }

    const total = entries.reduce((sum, [, value]) => sum + Number(value), 0);
    const radius = Math.min(width, height) * 0.28;
    const centerX = width * 0.34;
    const centerY = height * 0.5;
    let start = -Math.PI / 2;

    entries.forEach(([label, value], index) => {
        const angle = (Number(value) / total) * Math.PI * 2;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, start, start + angle);
        ctx.closePath();
        ctx.fillStyle = palette[index % palette.length];
        ctx.fill();
        start += angle;
        drawLegend(ctx, width * 0.65, 36 + index * 28, palette[index % palette.length], `${label} (${value})`);
    });
}

function drawBarChart(canvas, rawData) {
    const { ctx, width, height } = prepareCanvas(canvas);
    const entries = Object.entries(rawData).filter(([, value]) => Number(value) > 0);
    ctx.clearRect(0, 0, width, height);
    if (!entries.length) {
        drawEmpty(ctx, width, height);
        return;
    }

    const max = Math.max(...entries.map(([, value]) => Number(value)));
    const gap = 16;
    const chartTop = 22;
    const chartBottom = height - 44;
    const barWidth = (width - gap * (entries.length + 1)) / entries.length;

    entries.forEach(([label, value], index) => {
        const barHeight = (Number(value) / max) * (chartBottom - chartTop);
        const x = gap + index * (barWidth + gap);
        const y = chartBottom - barHeight;
        ctx.fillStyle = palette[index % palette.length];
        roundRect(ctx, x, y, Math.max(18, barWidth), barHeight, 8);
        ctx.fill();
        ctx.fillStyle = getTextColor();
        ctx.font = "700 12px system-ui";
        ctx.textAlign = "center";
        ctx.fillText(value, x + barWidth / 2, y - 8);
        ctx.fillText(label, x + barWidth / 2, height - 18);
    });
}

function drawLegend(ctx, x, y, color, text) {
    ctx.fillStyle = color;
    roundRect(ctx, x, y - 12, 14, 14, 4);
    ctx.fill();
    ctx.fillStyle = getTextColor();
    ctx.font = "700 13px system-ui";
    ctx.textAlign = "left";
    ctx.fillText(text, x + 22, y);
}

function drawEmpty(ctx, width, height) {
    ctx.fillStyle = getMutedColor();
    ctx.font = "700 15px system-ui";
    ctx.textAlign = "center";
    ctx.fillText("No data available", width / 2, height / 2);
}

function roundRect(ctx, x, y, width, height, radius) {
    const safeRadius = Math.min(radius, width / 2, Math.abs(height) / 2);
    ctx.beginPath();
    ctx.moveTo(x + safeRadius, y);
    ctx.lineTo(x + width - safeRadius, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + safeRadius);
    ctx.lineTo(x + width, y + height - safeRadius);
    ctx.quadraticCurveTo(x + width, y + height, x + width - safeRadius, y + height);
    ctx.lineTo(x + safeRadius, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - safeRadius);
    ctx.lineTo(x, y + safeRadius);
    ctx.quadraticCurveTo(x, y, x + safeRadius, y);
    ctx.closePath();
}

function getTextColor() {
    return getComputedStyle(document.documentElement).getPropertyValue("--text").trim() || "#0f172a";
}

function getMutedColor() {
    return getComputedStyle(document.documentElement).getPropertyValue("--muted").trim() || "#64748b";
}
