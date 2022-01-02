using Microsoft.AspNetCore.Mvc;

namespace statistics.templates
{
    public class ChartController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}
