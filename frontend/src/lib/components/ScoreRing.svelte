<script lang="ts">
  interface Props {
    score: number;
  }

  let { score }: Props = $props();

  let colour = $derived(
    score >= 80 ? '#34d399' : score >= 60 ? '#fbbf24' : '#f87171'
  );
  let label = $derived(
    score >= 80 ? 'Strong Match' : score >= 60 ? 'Needs Work' : 'Significant Gap'
  );

  // SVG circle calculations
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  let offset = $derived(circumference - (score / 100) * circumference);
</script>

<div class="flex flex-col items-center gap-3">
  <div class="relative h-36 w-36">
    <svg class="h-full w-full -rotate-90" viewBox="0 0 120 120">
      <!-- Background ring -->
      <circle
        cx="60" cy="60" r={radius}
        fill="none"
        stroke="currentColor"
        stroke-width="8"
        class="text-zinc-700"
      />
      <!-- Score ring -->
      <circle
        cx="60" cy="60" r={radius}
        fill="none"
        stroke={colour}
        stroke-width="8"
        stroke-linecap="round"
        stroke-dasharray={circumference}
        stroke-dashoffset={offset}
        class="transition-all duration-1000 ease-out"
      />
    </svg>
    <div class="absolute inset-0 flex flex-col items-center justify-center">
      <span class="text-3xl font-bold text-zinc-100">{score}</span>
      <span class="text-xs text-zinc-400">/ 100</span>
    </div>
  </div>
  <span class="text-sm font-medium" style="color: {colour}">{label}</span>
</div>
