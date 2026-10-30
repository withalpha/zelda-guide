// Cloudflare Pages Functions
// 禁用自动 .html 重定向，直接返回文件内容

export async function onRequest(context) {
  const { request, env, next } = context;
  
  // 获取响应
  const response = await next();
  
  // 如果是 308 重定向到无扩展名 URL，改为直接返回内容
  if (response.status === 308) {
    const url = new URL(request.url);
    
    // 如果请求的是 .html 文件，直接获取文件内容
    if (url.pathname.endsWith('.html')) {
      const asset = await env.ASSETS.fetch(request);
      return asset;
    }
  }
  
  return response;
}
