using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using GardenHelperWebAPI.Data;
using GardenHelperWebAPI.Models;


namespace GardenHelperWebAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class GardenersController : ControllerBase
    {
        private ApplicationDbContext _context;
        public GardenersController(ApplicationDbContext context)
        {
            _context = context;
        }
        // GET api/movie
        [HttpGet]
        public IActionResult Get()
        {
            var gardener = _context.Gardeners;
            return Ok(gardener);
        }
        
        [HttpGet("{id}")]
        public IActionResult Get(int id)
        {
            var gardener = _context.Gardeners.Where(m => m.Id == id);
            return Ok(gardener);
        }

        // POST api/movie
        [HttpPost]
        public IActionResult Post([FromBody] Gardener value)
        {
            _context.Gardeners.Add(value);
            _context.SaveChanges();
            return Ok();
        }

        // PUT api/movie
        [HttpPut]
        public IActionResult Put([FromBody] Gardener gardener)
        {
            _context.Gardeners.Update(gardener);
            _context.SaveChanges();
            return Ok();
        }

        
        [HttpDelete("{id}")]
        public IActionResult Delete(int id)
        {
            var selectedGardener = _context.Gardeners.FirstOrDefault(m => m.Id == id);
            _context.Gardeners.Remove(selectedGardener);
            _context.SaveChanges();
            return Ok();
        }
    }
}
