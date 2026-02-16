<script lang="ts">
  import { analysisState } from '$lib/stores';

  const messages: Record<string, string> = {
    uploading: 'Uploading resume...',
    analysing: 'Extracting text from PDF...',
    streaming: 'AI is analysing your resume...',
  };

  let dots = $state('');
  let interval: ReturnType<typeof setInterval>;

  $effect(() => {
    interval = setInterval(() => {
      dots = dots.length >= 3 ? '' : dots + '.';
    }, 500);

    return () => clearInterval(interval);
  });
</script>

{#if $analysisState === 'uploading' || $analysisState === 'analysing' || $analysisState === 'streaming'}
  <div class="flex flex-col items-center gap-4 py-12">
    <!-- Animated spinner -->
    <div class="relative h-12 w-12">
      <div class="absolute inset-0 rounded-full border-2 border-zinc-700"></div>
      <div class="absolute inset-0 animate-spin rounded-full border-2 border-transparent border-t-amber-400"></div>
    </div>
    <p class="text-sm text-zinc-400">
      {messages[$analysisState] ?? 'Processing...'}{dots}
    </p>
  </div>
{/if}
