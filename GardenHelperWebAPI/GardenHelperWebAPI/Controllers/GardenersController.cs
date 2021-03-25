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
    public class GardenersController : Controller
    {
        private readonly ApplicationDbContext _context;

        public GardenersController(ApplicationDbContext context)
        {
            _context = context;
        }

        // GET: Gardeners
        public async Task<IActionResult> Index()
        {
            return View(await _context.Gardener.ToListAsync());
        }

        // GET: Gardeners/Details/5
        public async Task<IActionResult> Details(int? id)
        {
            if (id == null)
            {
                return NotFound();
            }

            var gardener = await _context.Gardener
                .FirstOrDefaultAsync(m => m.Id == id);
            if (gardener == null)
            {
                return NotFound();
            }

            return View(gardener);
        }

        // GET: Gardeners/Create
        public IActionResult Create()
        {
            return View();
        }

        // POST: Gardeners/Create
        // To protect from overposting attacks, enable the specific properties you want to bind to, for 
        // more details, see http://go.microsoft.com/fwlink/?LinkId=317598.
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create([Bind("Id,FirstName,MiddleInitial,LastName,Email,AddressLine1,AddressLine2,City,State,Zip,Phone,Lat,Lng")] Gardener gardener)
        {
            if (ModelState.IsValid)
            {
                _context.Add(gardener);
                await _context.SaveChangesAsync();
                return RedirectToAction(nameof(Index));
            }
            return View(gardener);
        }

        // GET: Gardeners/Edit/5
        public async Task<IActionResult> Edit(int? id)
        {
            if (id == null)
            {
                return NotFound();
            }

            var gardener = await _context.Gardener.FindAsync(id);
            if (gardener == null)
            {
                return NotFound();
            }
            return View(gardener);
        }

        // POST: Gardeners/Edit/5
        // To protect from overposting attacks, enable the specific properties you want to bind to, for 
        // more details, see http://go.microsoft.com/fwlink/?LinkId=317598.
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(int id, [Bind("Id,FirstName,MiddleInitial,LastName,Email,AddressLine1,AddressLine2,City,State,Zip,Phone,Lat,Lng")] Gardener gardener)
        {
            if (id != gardener.Id)
            {
                return NotFound();
            }

            if (ModelState.IsValid)
            {
                try
                {
                    _context.Update(gardener);
                    await _context.SaveChangesAsync();
                }
                catch (DbUpdateConcurrencyException)
                {
                    if (!GardenerExists(gardener.Id))
                    {
                        return NotFound();
                    }
                    else
                    {
                        throw;
                    }
                }
                return RedirectToAction(nameof(Index));
            }
            return View(gardener);
        }

        // GET: Gardeners/Delete/5
        public async Task<IActionResult> Delete(int? id)
        {
            if (id == null)
            {
                return NotFound();
            }

            var gardener = await _context.Gardener
                .FirstOrDefaultAsync(m => m.Id == id);
            if (gardener == null)
            {
                return NotFound();
            }

            return View(gardener);
        }

        // POST: Gardeners/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteConfirmed(int id)
        {
            var gardener = await _context.Gardener.FindAsync(id);
            _context.Gardener.Remove(gardener);
            await _context.SaveChangesAsync();
            return RedirectToAction(nameof(Index));
        }

        private bool GardenerExists(int id)
        {
            return _context.Gardener.Any(e => e.Id == id);
        }
    }
}
