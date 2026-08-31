/**
 * StudyChart AI - HTML5 Canvas Interactive Chart Engine.
 * Lightweight, zero-dependency, retina-ready, theme-aware charting.
 */

export class ChartEngine {
  static setupCanvas(canvas) {
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    const ctx = canvas.getContext("2d");
    ctx.scale(dpr, dpr);
    return { ctx, width: rect.width, height: rect.height };
  }

  static renderBarChart(canvasId, labels, dataPoints, color = "#6366f1") {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    const { ctx, width, height } = this.setupCanvas(canvas);
    ctx.clearRect(0, 0, width, height);

    const padding = { top: 30, right: 20, bottom: 40, left: 50 };
    const chartW = width - padding.left - padding.right;
    const chartH = height - padding.top - padding.bottom;

    const maxVal = Math.max(...dataPoints, 60);
    const barWidth = Math.min(45, (chartW / labels.length) * 0.55);
    const gap = chartW / labels.length;

    // Draw grid lines
    ctx.strokeStyle = "rgba(156, 163, 175, 0.15)";
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
      const y = padding.top + (chartH / 4) * i;
      ctx.beginPath();
      ctx.moveTo(padding.left, y);
      ctx.lineTo(width - padding.right, y);
      ctx.stroke();

      const labelVal = Math.round(maxVal - (maxVal / 4) * i);
      ctx.fillStyle = "#9ca3af";
      ctx.font = "11px Inter, sans-serif";
      ctx.textAlign = "right";
      ctx.fillText(`${labelVal}m`, padding.left - 10, y + 4);
    }

    // Draw bars
    labels.forEach((label, idx) => {
      const val = dataPoints[idx] || 0;
      const barH = (val / maxVal) * chartH;
      const x = padding.left + gap * idx + (gap - barWidth) / 2;
      const y = padding.top + chartH - barH;

      // Gradient fill
      const grad = ctx.createLinearGradient(0, y, 0, y + barH);
      grad.addColorStop(0, color);
      grad.addColorStop(1, "#a855f7");

      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.roundRect(x, y, barWidth, barH, [6, 6, 0, 0]);
      ctx.fill();

      // X labels
      ctx.fillStyle = "#9ca3af";
      ctx.font = "12px Inter, sans-serif";
      ctx.textAlign = "center";
      ctx.fillText(label, x + barWidth / 2, height - 15);
    });
  }

  static renderDonutChart(canvasId, items) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    const { ctx, width, height } = this.setupCanvas(canvas);
    ctx.clearRect(0, 0, width, height);

    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(centerX, centerY) * 0.75;
    const innerRadius = radius * 0.6;

    const total = items.reduce((sum, item) => sum + item.value, 0);
    if (total === 0) {
      ctx.fillStyle = "#374151";
      ctx.beginPath();
      ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
      ctx.arc(centerX, centerY, innerRadius, 2 * Math.PI, 0, true);
      ctx.fill();
      return;
    }

    let startAngle = -Math.PI / 2;

    items.forEach(item => {
      const sliceAngle = (item.value / total) * 2 * Math.PI;
      const endAngle = startAngle + sliceAngle;

      ctx.fillStyle = item.color || "#6366f1";
      ctx.beginPath();
      ctx.arc(centerX, centerY, radius, startAngle, endAngle);
      ctx.arc(centerX, centerY, innerRadius, endAngle, startAngle, true);
      ctx.closePath();
      ctx.fill();

      startAngle = endAngle;
    });

    // Center text
    ctx.fillStyle = "#f9fafb";
    ctx.font = "bold 16px Inter, sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(`${total}m`, centerX, centerY + 5);
  }
}
