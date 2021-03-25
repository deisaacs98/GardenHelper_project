using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;
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
            // Retrieve all movies from db logic
            var gardener = _context.Gardeners;
            return Ok(gardener);
        }

        // GET api/movie/5
        [HttpGet("{id}")]
        public IActionResult Get(int id)
        {
            // Retrieve movie by id from db logic
            // return Ok(movie);
            var movie = _context.Gardeners.Where(m => m.Id == id);
            return Ok(movie);
        }

        // POST api/movie
        [HttpPost]
        public IActionResult Post([FromBody] Gardener value)
        {
            // Create movie in db logic
            _context.Gardeners.Add(value);
            _context.SaveChanges();
            return Ok();
        }

        // PUT api/movie
        [HttpPut]
        public IActionResult Put([FromBody] Gardener gardener)
        {
            // Update movie in db logic
            _context.Gardeners.Update(gardener);
            _context.SaveChanges();
            return Ok();
        }

        // DELETE api/movie/5
        [HttpDelete("{id}")]
        public IActionResult Delete(int id)
        {
            // Delete movie from db logic
            var selectedGardener = _context.Gardeners.FirstOrDefault(m => m.Id == id);
            _context.Gardeners.Remove(selectedGardener);
            _context.SaveChanges();
            return Ok();
        }
    }
}
